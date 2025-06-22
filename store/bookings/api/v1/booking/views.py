from .serializers import SlotBookingSerializer, BookingListModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from store.bookings.models import BookingsModel
from coreutils.utils.generics.views.generic_views import (
    CoreGenericPostAPIView,
    CoreGenericListAPIView,
)
from rest_framework import generics
from store.bookings.api.v1.utils.constants import SLOT_BOOKING_SUCCESS_MESSAGE
from store.bookings.api.v1.utils.filterset import BookingsModelFilterSet


class SlotBookingAPIView(
    CoreGenericPostAPIView,
    generics.GenericAPIView,
):
    queryset = BookingsModel.objects.all()
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    success_message = SLOT_BOOKING_SUCCESS_MESSAGE

    def get_serializer_class(self):
        serializer_class = {"POST": SlotBookingSerializer}
        return serializer_class.get(self.request.method)


class BookingsListAPIView(CoreGenericListAPIView, generics.ListAPIView):
    queryset = BookingsModel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookingsModelFilterSet

    def get_serializer_class(self):
        serializer_class = {"GET": BookingListModelSerializer}
        return serializer_class.get(self.request.method)
