from django.db.models.query import QuerySet
from django.db.models import Model
from coreutils.utils.generics.views.queryset import (
    CoreGenericQueryset,
    CoreGenericQuerysetInstance,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
from typing import Dict, Any, List
from coreutils.utils.generics.views.process_view import (
    CoreGenericProcessDataAPIView,
    CoreGenericProcessDataModelSerializerAPIView,
)
from coreutils.utils.generics.views.core_generic_utils import CoreGenericUtils


class CoreGenericListAPIView(CoreGenericQueryset):
    """
    Generic GET API for returning a paginated queryset of model instances.

    This class expects a valid queryset and a serializer class.
    It handles pagination and returns serialized data accordingly.
    """

    queryset: QuerySet[Model]

    def list(self, request: Request, *args: List, **kwargs: Dict):
        """
        GET handler for listing model instances in a paginated format.

        Returns:
            - Paginated response with serialized model data.
        Raises:
            - Any error is caught and passed to the custom exception handler.
        """
        try:
            if self.check_custom_permission():
                return Response(
                    {"message": self.UNAUTHZORIZED_ACTION_ERROR_MESSAGE},
                    status=status.HTTP_403_FORBIDDEN,
                )
            # ? Get paginated queryset from CoreGenericQueryset
            queryset = self.filter_queryset(self.get_queryset())
            paginated_queryset: QuerySet[Model] = self.paginate_queryset(queryset)

            # ? Prepare context for serializer (can include request/user/etc.)
            context: Dict[Any] = self.set_context_data()

            # ? Serialize data
            serializer: Serializer = self.get_serializer(
                paginated_queryset, context=context, many=True
            )

            # ? Return paginated response with serialized data
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            # ? Custom exception handler
            return self.custom_handle_exception(e=e)


class CoreGenericGetAPIView(CoreGenericQueryset, CoreGenericQuerysetInstance):
    """
    Generic GET API for returning one or more model instances based on the `many` flag.

    Attributes:
        many (bool):
            - True: Returns a queryset (list of objects).
            - False: Returns a single model instance.
    """

    queryset: QuerySet[Model]
    many: bool = True
    skip_validation: bool = False
    INCORRECT_ID_EXCEPTION = {
        "title": "Incorrect Id",
        "description": "Entered Id is incorrect or records does not existing",
    }

    def get(self, request: Request, *args: List, **kwargs: Dict):
        """
        GET handler for retrieving data using a serializer.

        Returns:
            - List or single object based on the `many` flag.
        """
        try:
            if self.check_custom_permission():
                return Response(
                    {"message": self.UNAUTHZORIZED_ACTION_ERROR_MESSAGE},
                    status=status.HTTP_403_FORBIDDEN,
                )
            validations: str | None = self.get_object_pk_validation()
            if validations:
                return self.validation_response(
                    validated_data={"error_message": validations}
                )
            # ? Fetch queryset or single object
            if self.many:
                queryset: QuerySet[Model] = self.filter_queryset(self.get_queryset())
            else:
                queryset: Model = self.get_object()

            # ? Prepare context and serialize data
            context: Dict[Any] = self.set_context_data()
            serializer: Serializer = self.get_serializer(
                queryset, context=context, many=self.many
            )

            return self.success_response(validated_data=serializer.data)
        except Exception as e:
            return self.custom_handle_exception(e)


class CoreGenericGetDataFromSerializerAPIView(
    CoreGenericGetAPIView, CoreGenericQueryset, CoreGenericProcessDataAPIView
):
    """
    GET API that executes business logic within a serializer.

    Use this when data needs to be calculated/processed via serializer logic
    (using `validate()` and `create()`) which are return inside handlers,
    rather than direct DB reads.
    """

    def get(self, request: Request, *args: List, **kwargs: Dict):
        """
        GET handler that routes logic through `handle_request()`
        which invokes validation and creation logic in the serializer.
        """
        return self.handle_request()


class CoreGenericGetPaginatedDataFromSerializerAPIView(
    CoreGenericQueryset, CoreGenericProcessDataAPIView
):
    """
    GET API that returns a paginated response using custom serializer logic.

    The serializer’s `validate()` and `create()` methods which are return inside handlers
    are used to process and return custom paginated data.
    """

    def get(self, request: Request, *args: List, **kwargs: Dict):
        """
        GET handler for returning paginated serializer-driven data.
        """
        return self.get_custom_paginated_response()


class CoreGenericPostAPIView(
    CoreGenericProcessDataAPIView,
    CoreGenericUtils,
):
    """
    Generic POST API that processes input through a serializer.

    Useful when the logic resides inside the serializer’s `validate()`
    and `create()` methods which are return inside handlers.
    """

    def post(self, request: Request, *args: List, **kwargs: Dict):
        """
        POST handler that passes request data through serializer logic.
        """
        return self.handle_request()


class CoreGenericCreateAPIView(
    CoreGenericProcessDataAPIView,
    CoreGenericUtils,
):
    """
    View for executing create logic that is not necessarily tied to POST.

    Can be called internally or used for business logic simulations.
    """

    def create(self, request: Request, *args: List, **kwargs: Dict):
        """
        Handler for executing creation logic through a serializer.
        """
        return self.handle_request()


class CoreGenericListCreateAPIView(CoreGenericCreateAPIView, CoreGenericListAPIView):
    """
    Combines list and create views into a single view class.

    Supports:
        - GET: Paginated listing of model data
        - CREATE: Serializer-based object creation
    """


class CoreGenericPutAPIView(
    CoreGenericProcessDataAPIView,
    CoreGenericUtils,
):
    """
    Generic PUT API to process update requests through custom logic.

    Ideal when you need validation and transformation before updating.
    """

    def put(self, request: Request, *args: List, **kwargs: Dict):
        """
        PUT handler for updating data via serializer logic.
        """
        return self.handle_request()


class CoreGenericPutModelSerializerAPIView(
    CoreGenericProcessDataModelSerializerAPIView,
    CoreGenericUtils,
):
    """
    PUT API for updating model instances using standard Django model serializers.

    Suitable for cases where you want to update model fields directly.
    """

    def put(self, request: Request, *args: List, **kwargs: Dict):
        """
        PUT handler for model instance updates.
        """
        return self.handle_request()


class CoreGenericDeleteAPIView(
    CoreGenericProcessDataAPIView,
    CoreGenericUtils,
):
    """
    Generic DELETE API to handle deletion logic through serializers.

    Use this when business rules are involved in deletion,
    such as soft deletes, cascading checks, etc.
    """

    def delete(self, request: Request, *args: List, **kwargs: Dict):
        """
        DELETE handler that delegates logic to serializer.
        """
        return self.handle_request()
