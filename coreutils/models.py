from django.db import models
from coreutils.utils.generics.generic_models import CoreGenericModel
import uuid

# Create your models here.


class WeekDayOffModel(CoreGenericModel):
    "Defines weekly holidays for the scheduling system."

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="ID",
        editable=False,
    )
    IS_MONDAY_HOLIDAY = models.BooleanField(
        default=False, db_column="IS_MONDAY_HOLIDAY"
    )
    IS_TUESDAY_HOLIDAY = models.BooleanField(
        default=False, db_column="IS_TUESDAY_HOLIDAY"
    )
    IS_WEDNSDAY_HOLIDAY = models.BooleanField(
        default=False, db_column="IS_WEDNSDAY_HOLIDAY"
    )
    IS_THURSDAY_HOLIDAY = models.BooleanField(
        default=False, db_column="IS_THURSDAY_HOLIDAY"
    )
    IS_FRIDAY_HOLIDAY = models.BooleanField(
        default=False, db_column="IS_FRIDAY_HOLIDAY"
    )
    IS_SATURDAY_HOLIDAY = models.BooleanField(
        default=False, db_column="IS_SATURDAY_HOLIDAY"
    )
    IS_SUNDAY_HOLIDAY = models.BooleanField(
        default=False, db_column="IS_SUNDAY_HOLIDAY"
    )

    class Meta:
        db_table = "WEEK_OF_DAYS"
