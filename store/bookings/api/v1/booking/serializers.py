from rest_framework import serializers
from store.bookings.models import BookingsModel
from coreutils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from store.bookings.api.v1.utils.handlers.booking_handler import BookingHandler


class SlotBookingSerializer(CoreGenericSerializerMixin, serializers.Serializer):
    queryset = BookingsModel.objects.all()
    class_id = serializers.UUIDField()
    client_name = serializers.CharField()
    client_email = serializers.EmailField()
    handler_class = BookingHandler
