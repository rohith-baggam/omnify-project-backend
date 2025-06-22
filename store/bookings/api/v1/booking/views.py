from .serializers import SlotBookingSerializer
from django.contrib.auth import get_user_model
from coreutils.utils.generics.views.generic_views import CoreGenericPostAPIView
from rest_framework import generics
from store.bookings.api.v1.utils.constants import SLOT_BOOKING_SUCCESS_MESSAGE


class SlotBookingAPIView(
    CoreGenericPostAPIView,
    generics.GenericAPIView,
):
    queryset = get_user_model().objects.all()
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    success_message = SLOT_BOOKING_SUCCESS_MESSAGE

    def get_serializer_class(self):
        serializer_class = {"POST": SlotBookingSerializer}
        return serializer_class.get(self.request.method)
