from django.db import models
from coreutils.utils.generics.generic_models import CoreGenericModel
import uuid
from store.classes.models import ClassAssignedInstructorModel


class SlotTimigsModel(CoreGenericModel):
    "Defines available time slots for classes."

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="ID",
        editable=False,
    )
    start_time = models.TimeField(db_column="START_TIME")
    end_time = models.TimeField(db_column="END_TIME")
    max_no_of_attendies = models.IntegerField(db_column="MAX_NO_OF_ATTENDIES")

    class Meta:
        db_table = "SLOT_TIMINGS_TABLE"

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class AssignedSlotsTimingsToClassesModel(CoreGenericModel):
    "Assigns specific time slots to instructor-class pairs."

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="ID",
        editable=False,
    )
    class_id = models.ForeignKey(
        ClassAssignedInstructorModel,
        on_delete=models.CASCADE,
        related_name="AssignedSlotsTimingsToClassesModel_class_id",
        db_column="CLASS",
    )
    slot_id = models.ForeignKey(
        SlotTimigsModel,
        on_delete=models.CASCADE,
        related_name="AssignedSlotsTimingsToClassesModel_slot_id",
        db_column="SLOTS",
    )

    class Meta:
        db_table = "ASSIGNED_SLOTS_TIMINGS_TO_CLASSES_TABLE"
        unique_together = ("class_id", "slot_id")

    def __str__(self):
        return f"{self.class_id.classes.title} - {self.slot_id.start_time}"
