from coreutils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from typing import Dict


class CoreGenericMultiDeleteHandler(CoreGenericBaseHandler):
    """
    Handles custom multi-delete validation and execution logic for queryset objects.
    """

    incorrect_delete_id_message: Dict = {
        "title": "Delete ID",
        "description": "One or more provided delete IDs are invalid.",
    }

    def validate(self):
        """
        Validates whether provided delete IDs exist in the queryset.
        Adds error message to data if validation fails.
        """
        if not self.queryset.filter(pk__in=self.data["delete_id"]).exists():
            self.data["error_message"] = self.incorrect_delete_id_message

    def create(self):
        """
        Executes deletion of objects with provided primary keys.
        """
        self.queryset.filter(pk__in=self.data["delete_id"]).delete()
