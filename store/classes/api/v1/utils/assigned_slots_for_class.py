from datetime import datetime
from django.utils.timezone import localtime
from django.db.models import Count, F, Q
from django.db.models.query import QuerySet
from store.slots.models import AssignedSlotsTimingsToClassesModel
from store.bookings.models import BookingsModel
from store.classes.models import ClassAssignedInstructorModel
from typing import Dict
from django.utils.timezone import now as django_now


def get_assigned_slots_queryset(
    assigned_class_instance: ClassAssignedInstructorModel, params: Dict
) -> QuerySet[AssignedSlotsTimingsToClassesModel]:
    """
    Returns assigned slots excluding:
    - slots fully booked on given date
    - slots with end_time < current time (only if for today)
    - slots falling on weekday holidays
    """
    target_date = datetime.strptime(params["date_of_booking"], "%Y-%m-%d").date()

    today = django_now().date()
    current_time = localtime(django_now()).time()

    # Step 1: Get slots for the given class
    assigned_slots_queryset: QuerySet[
        AssignedSlotsTimingsToClassesModel
    ] = AssignedSlotsTimingsToClassesModel.objects.filter(
        class_id=assigned_class_instance
    ).annotate(
        booking_count=Count(
            "BookingsModel_slot",
            filter=Q(BookingsModel_slot__date_of_booking=target_date),
        )
    )

    # Step 2: Filter out fully booked slots
    assigned_slots_queryset: QuerySet[AssignedSlotsTimingsToClassesModel] = (
        assigned_slots_queryset.exclude(
            booking_count__gte=F("slot_id__max_no_of_attendies")
        )
    )

    # Step 3: If booking for today, exclude slots that have already ended
    if target_date == today:
        assigned_slots_queryset: QuerySet[AssignedSlotsTimingsToClassesModel] = (
            assigned_slots_queryset.exclude(slot_id__end_time__lte=current_time)
        )

    # Step 4: Exclude slots based on weekday holiday
    weekday: int = target_date.weekday()  # Monday=0 ... Sunday=6
    week_off_field_map: Dict = {
        0: "class_id__week_days_off__IS_MONDAY_HOLIDAY",
        1: "class_id__week_days_off__IS_TUESDAY_HOLIDAY",
        2: "class_id__week_days_off__IS_WEDNSDAY_HOLIDAY",
        3: "class_id__week_days_off__IS_THURSDAY_HOLIDAY",
        4: "class_id__week_days_off__IS_FRIDAY_HOLIDAY",
        5: "class_id__week_days_off__IS_SATURDAY_HOLIDAY",
        6: "class_id__week_days_off__IS_SUNDAY_HOLIDAY",
    }
    holiday_filter: Dict = {week_off_field_map[weekday]: True}
    assigned_slots_queryset = assigned_slots_queryset.exclude(**holiday_filter)

    return assigned_slots_queryset


def get_assigned_slots_for_classes(
    assigned_class_instance: ClassAssignedInstructorModel, params: Dict
):
    assigned_slots_queryset: QuerySet[AssignedSlotsTimingsToClassesModel] = (
        get_assigned_slots_queryset(
            assigned_class_instance=assigned_class_instance, params=params
        )
    )

    return assigned_slots_queryset.values(
        "id",
        "slot_id__start_time",
        "slot_id__end_time",
        "slot_id__max_no_of_attendies",
    )
