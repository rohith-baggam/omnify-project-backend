from store.bookings.api.v1.booking import views
from django.urls import path

urlpatterns = [
    path("book/", views.SlotBookingAPIView.as_view(), name="SlotBookingAPIView"),
    path("bookings/", views.BookingsListAPIView.as_view(), name="BookingsListAPIView"),
]
