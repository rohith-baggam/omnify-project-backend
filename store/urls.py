from django.urls import path, include

urlpatterns = [
    path("classes/api/v1/", include("store.classes.api.v1.urls")),
    path("bookings/api/v1/", include("store.bookings.api.v1.urls")),
]
