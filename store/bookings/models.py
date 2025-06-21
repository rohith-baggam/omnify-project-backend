from django.db import models
from coreutils.utils.generics.generic_models import CoreGenericModel
import uuid
from django.contrib.auth import get_user_model
from store.slots.models import AssignedSlotsTimingsToClassesModel

# Create your models here.
# BOOKING_TABLE


class BookingsModel(CoreGenericModel):
    "Records bookings made by clients for specific slots."

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="ID",
        editable=False,
    )
    client = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="BookingsModel_client",
        db_column="CLIENT_ID",
    )
    slot = models.ForeignKey(
        AssignedSlotsTimingsToClassesModel,
        on_delete=models.CASCADE,
        related_name="BookingsModel_slot",
        db_column="SLOT_ID",
    )
    date_of_booking = models.DateField(db_column="DATE_OF_BOOKING")

    class Meta:
        db_table = "BOOKING_TABLE"
        unique_together = ("client", "slot", "date_of_booking")
