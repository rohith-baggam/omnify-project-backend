from django.db import models
from coreutils.utils.generics.generic_models import CoreGenericModel
import uuid
from django.contrib.auth import get_user_model
from coreutils.models import WeekDayOffModel

# Create your models here.


class ClassesModel(CoreGenericModel):
    "Stores information related to different classes."

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="ID",
        editable=False,
    )
    title = models.CharField(max_length=256, unique=True, db_column="TITLE")
    description = models.TextField(db_column="DESCRIPTION")

    class Meta:
        db_table = "CLASSES_TABLE"

    def __str__(self):
        return self.title


class ClassAssignedInstructorModel(CoreGenericModel):
    "Defines available slot details like timing and attendies."

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="ID",
        editable=False,
    )
    instructor = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="ClassAssignedInstructorModel_instructor",
        db_column="USER_ASSIGNED",
    )
    classes = models.ForeignKey(
        ClassesModel,
        on_delete=models.CASCADE,
        related_name="ClassAssignedInstructorModel_classes",
        db_column="CLASS_ASSIGNED",
    )
    week_days_off = models.ForeignKey(
        WeekDayOffModel,
        on_delete=models.CASCADE,
        related_name="ClassAssignedInstructorModel_week_days_off",
        db_column="WEEK_OFF_DAYS",
    )

    class Meta:
        db_table = "CLASSES_ASSIGNED_INSTRUCTOR_TABLE"
        unique_together = ("instructor", "classes")

    def __str__(self):
        return f"{self.classes.title} -> {self.instructor.username}"
