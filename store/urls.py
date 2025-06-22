from django.urls import path, include

urlpatterns = [path("classes/api/v1/", include("store.classes.api.v1.urls"))]
