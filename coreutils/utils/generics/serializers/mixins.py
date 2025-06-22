from django.db.models.query import QuerySet
from django.db.models import Model
from typing import Dict, Type, List, Callable, Union
from coreutils.utils.generics.serializers.generic_serializers import (
    CoreGenericGetQuerysetSerializer,
)
from django.db.models.query import QuerySet
from django.db.models import Model
from rest_framework.request import Request


class CoreGenericSerializerMixin(CoreGenericGetQuerysetSerializer):
    """
    A reusable mixin to integrate custom validator logic for DRF serializers.
    This mixin supports custom validation and object creation logic using
    external handler classes.
    """

    custom_validator: Type
    queryset: QuerySet[Model]
    api_data: dict = {}
    handler_class: (
        Type  # Must be overridden by subclasses to specify the validator class
    )

    def set_validator(self):
        """
        Instantiates the handler class with request and queryset context.

        Returns:
            Type: Initialized handler instance.
        """
        self.custom_validator = self.handler_class(
            request=self.context["request"], queryset=self.get_queryset()
        )
        return self.custom_validator

    def custom_validate(self, data: Dict):
        """
        Performs custom validation using the provided handler.

        Args:
            data (Dict): Input data for validation.
        """
        self.set_validator()
        self.custom_validator.set_data(data=data)
        self.custom_validator.validate()
        self.api_data = data

    def validate(self, data: Dict):
        """
        DRF validate method override to apply custom validation logic.

        Args:
            data (Dict): Input data.

        Returns:
            Dict: Validated data.
        """
        self.custom_validate(data)
        return data

    def create(self, validated_data: Dict):
        """
        Triggers creation logic using the handler.

        Args:
            validated_data (Dict): Data after validation.

        Returns:
            Dict: Final validated data after handler execution.
        """
        self.custom_validator.create()
        return validated_data


class CoreGenericBaseHandler:
    """
    Handler class for converting uploaded files to URLs and saving metadata
    using a configurable storage convertor (local/S3/etc.).

    Designed to integrate with serializers and views for file handling logic.

    Note :
        As this is a constructor class always keep first preference while inheriting
    """

    request: Request
    data: Dict
    queryset: QuerySet[Model]

    def __init__(self, request: Request, queryset: QuerySet):
        """
        Initialize the handler with request and queryset context.

        :param request: The incoming DRF request containing files and user
        :param queryset: Associated queryset context (optional use-case)
        """
        self.request: Request = request
        self.queryset: QuerySet[Model] = queryset

    def set_data(self, data: Dict):
        """
        Attach validated serializer data to the handler instance.

        :param data: Dictionary containing validated data (usually from serializer)
        """
        self.data: Dict = data

    def check_validation_classes(
        self, validation_methods_list: List[List[Union[Callable, Dict]]]
    ) -> bool:
        for validation in validation_methods_list:
            validation_methods: Callable = validation[0]
            args: Dict = validation[1]
            if validation_methods(**args):
                return True
        return False

    def set_error_message(
        self, error_message: Dict, key: str = "", is_field_errors: bool = False
    ):
        if key:
            if is_field_errors:
                error_message: Dict = {
                    "title": error_message["title"],
                    "description": key + " " + error_message["description"],
                }
            if not self.data.get("field_errors"):
                self.data["field_errors"] = {}
            self.data["field_errors"][key] = error_message["description"]
        self.data["error_message"] = error_message

    def get_request_kwargs(
        self,
    ) -> Dict:
        """
        Returns the dict of kwargs from the request
        """
        return self.request.parser_context["kwargs"]

    def validate(self):
        pass

    def create(self):
        pass
