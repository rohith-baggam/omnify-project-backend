from store.slots.models import AssignedSlotsTimingsToClassesModel
from django.db.models.query import QuerySet
from store.classes.models import ClassAssignedInstructorModel


def get_assigned_slots_queryset(
    assigned_class_instance: ClassAssignedInstructorModel,
) -> QuerySet[AssignedSlotsTimingsToClassesModel]:
    assigned_slots_queryset: QuerySet[AssignedSlotsTimingsToClassesModel] = (
        AssignedSlotsTimingsToClassesModel.objects.filter(
            class_id=assigned_class_instance
        )
    )
    return assigned_slots_queryset


def get_assigned_slots_for_classes(
    assigned_class_instance: ClassAssignedInstructorModel,
):
    assigned_slots_queryset: QuerySet[AssignedSlotsTimingsToClassesModel] = (
        get_assigned_slots_queryset(assigned_class_instance=assigned_class_instance)
    )

    return assigned_slots_queryset.values(
        "slot_id__start_time",
        "slot_id__end_time",
        "slot_id__max_no_of_attendies",
    )
