from django.urls import path
from store.classes.api.v1.slots_list import views

urlpatterns = [
    path(
        "classes/", views.ClassListModelAPIView.as_view(), name="ClassListModelAPIView"
    )
]
