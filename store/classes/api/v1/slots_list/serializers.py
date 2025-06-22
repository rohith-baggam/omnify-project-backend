from store.classes.models import ClassAssignedInstructorModel
from rest_framework import serializers
from coreutils.models import WeekDayOffModel
from typing import List, Dict
from store.classes.api.v1.utils.assigned_slots_for_class import (
    get_assigned_slots_for_classes,
)


class ClassListModelSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source="classes.title", default=None)
    instructor = serializers.CharField(source="instructor.username", default=None)
    week_days_off = serializers.SerializerMethodField()
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = ClassAssignedInstructorModel
        fields = ["id", "class_name", "instructor", "week_days_off", "available_slots"]

    def get_week_days_off(self, obj: ClassAssignedInstructorModel):
        week_days_off_instance: WeekDayOffModel = obj.week_days_off
        week_days_off: List[str] = []
        days: List[str] = [
            "IS_MONDAY_HOLIDAY",
            "IS_TUESDAY_HOLIDAY",
            "IS_WEDNSDAY_HOLIDAY",
            "IS_THURSDAY_HOLIDAY",
            "IS_FRIDAY_HOLIDAY",
            "IS_SATURDAY_HOLIDAY",
            "IS_SUNDAY_HOLIDAY",
        ]
        for day in days:
            if getattr(week_days_off_instance, day, False):
                week_days_off.append(str(day).split("_")[1])

        return week_days_off

    def get_available_slots(self, obj: ClassAssignedInstructorModel) -> List[Dict]:
        try:
            return get_assigned_slots_for_classes(assigned_class_instance=obj)
        except Exception as e:
            print(e)
            return []


# name, date/time, instructor, available slots
