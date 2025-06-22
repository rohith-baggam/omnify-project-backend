from store.bookings.models import BookingsModel
from django.db import transaction
from django.db.models.query import QuerySet
from coreutils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from userauth.models import UserModel
from django.contrib.auth import get_user_model
from store.slots.models import AssignedSlotsTimingsToClassesModel
from typing import Dict
from django.utils.timezone import now as django_now


class BookingHandler(CoreGenericBaseHandler):
    """
    Handler for creating bookings for assigned slots.

    Expects the following keys in `self.data`:
    - class_id: ID of the class (AssignedSlotsTimingsToClassesModel)
    - client_name: Name of the client
    - client_email: Email of the client
    """

    # ? Instance-level reference to the assigned slot class (populated during validation)
    assigned_slots_timings_to_class_instance: AssignedSlotsTimingsToClassesModel

    def validate_class_id(
        self,
        assigned_slots_timings_to_class_queryset: QuerySet[
            AssignedSlotsTimingsToClassesModel
        ],
    ) -> Dict:
        """
        Validates the class ID provided in self.data:
        - Checks if the class ID exists.
        - Prevents duplicate bookings by the same client for the same slot.
        - Prevents overbooking beyond the slot's capacity.

        Args:
            assigned_slots_timings_to_class_queryset (QuerySet): Queryset of all class assignments.

        Returns:
            Dict: Error message dict if validation fails, otherwise an empty dict.
        """
        error_message: Dict = {}

        # ? Check if the class ID exists
        if not assigned_slots_timings_to_class_queryset.filter(
            pk=self.data["class_id"]
        ).exists():
            return {"title": "Incorrect Id", "description": "class id is incorrect"}

        # ? Retrieve the class instance
        self.assigned_slots_timings_to_class_instance = (
            assigned_slots_timings_to_class_queryset.get(pk=self.data["class_id"])
        )

        booking_queryset = BookingsModel.objects.all()

        # ? Check if this client has already booked this slot
        if booking_queryset.filter(
            slot=self.assigned_slots_timings_to_class_instance,
            client__email=self.data["client_email"],
        ).exists():
            return {
                "title": "Already booked",
                "description": "You have already booked for this slot",
            }

        # ? Check if the slot is fully booked for today's date
        if (
            booking_queryset.filter(
                slot=self.assigned_slots_timings_to_class_instance,
                date_of_booking=django_now().date(),
            ).count()
            == self.assigned_slots_timings_to_class_instance.slot_id.max_no_of_attendies
        ):
            return {
                "title": "Slot's are filled",
                "description": "max people are filled for this slot",
            }

        return error_message

    def validate(self):
        """
        Executes all necessary validations before creating a booking.
        Adds any validation errors using `set_error_message`.
        """
        assigned_slots_timings_to_class_queryset = (
            AssignedSlotsTimingsToClassesModel.objects.all()
        )

        class_id_error_message = self.validate_class_id(
            assigned_slots_timings_to_class_queryset=assigned_slots_timings_to_class_queryset
        )

        if class_id_error_message:
            return self.set_error_message(
                error_message=class_id_error_message,
                key="class_id",
            )

    def get_user_instance(self) -> UserModel:
        """
        Retrieves or creates a UserModel instance based on client_email.

        Returns:
            UserModel: The existing or newly created user.
        """
        user_queryset = get_user_model().objects.all()

        if user_queryset.filter(email=self.data["client_email"]).exists():
            user_instance = user_queryset.get(email=self.data["client_email"])
        else:
            user_instance = user_queryset.create(
                username=self.data["client_name"],
                email=self.data["client_email"],
                is_active=True,
                is_verified=True,
                is_approved=True,
                is_client=True,
            )
        return user_instance

    def create(self):
        """
        Creates a new booking for the validated slot and client.
        Executes within an atomic transaction to ensure consistency.
        """
        with transaction.atomic():
            user_instance = self.get_user_instance()
            self.queryset.create(
                client=user_instance,
                slot=self.assigned_slots_timings_to_class_instance,
                date_of_booking=django_now().date(),
            )
