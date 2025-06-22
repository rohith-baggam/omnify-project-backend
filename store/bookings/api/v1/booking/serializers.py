from rest_framework import serializers
from store.bookings.models import BookingsModel
from coreutils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from store.bookings.api.v1.utils.handlers.booking_handler import BookingHandler
from store.classes.models import ClassesModel
from userauth.models import UserModel
from store.slots.models import SlotTimigsModel


class SlotBookingSerializer(CoreGenericSerializerMixin, serializers.Serializer):
    queryset = BookingsModel.objects.all()
    class_id = serializers.UUIDField()
    client_name = serializers.CharField()
    client_email = serializers.EmailField()
    date_of_booking = serializers.DateField()
    handler_class = BookingHandler


class BookingListModelSerializer(serializers.ModelSerializer):
    client_details = serializers.SerializerMethodField()
    instructor_details = serializers.SerializerMethodField()
    class_details = serializers.SerializerMethodField()
    slot_details = serializers.SerializerMethodField()

    class Meta:
        model = BookingsModel
        fields = [
            "id",
            "client_details",
            "instructor_details",
            "class_details",
            "slot_details",
            "date_of_booking",
        ]

    def get_client_details(self, obj: BookingsModel):
        try:
            data = {
                "user_id": obj.client.username,
                "username": obj.client.username,
                "email": obj.client.email,
            }
        except:
            data = {}
        return data

    def get_instructor_details(self, obj: BookingsModel):
        try:
            instructor_instance: UserModel = obj.slot.class_id.instructor
            data = {
                "user_id": instructor_instance.username,
                "username": instructor_instance.username,
                "email": instructor_instance.email,
            }
        except Exception as e:
            data = {}
        return data

    def get_class_details(self, obj: BookingsModel):
        try:
            class_instance: ClassesModel = obj.slot.class_id.classes
            data = {"id": class_instance.pk, "class_name": class_instance.title}
        except:
            data = {}
        return data

    def get_slot_details(self, obj: BookingsModel):
        try:
            slot_instance: SlotTimigsModel = obj.slot.slot_id
            data = {
                "slot_id": slot_instance.pk,
                "start_time": slot_instance.start_time,
                "end_time": slot_instance.end_time,
                "max_no_of_attendies": slot_instance.max_no_of_attendies,
            }
        except:
            data = {}
        return data
