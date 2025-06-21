from django.db.models.query import QuerySet
from django.db.models import Model
from typing import Dict, Union, List, Optional
from rest_framework.response import Response
from rest_framework import status
from core.settings import logger
import logging
import inspect
import uuid


class CoreGenericUtils:
    """
    A utility mixin class providing common methods for API views and other classes
    working with Django models and DRF views.
    """

    queryset: QuerySet  # Expected to be set by a subclass or external assignment

    def get_logger(self) -> logging.LoggerAdapter:
        """
        Creates and returns a LoggerAdapter instance with context-specific information.

        Returns:
            logging.LoggerAdapter: Logger adapter including class name and file path.
        """
        frame: inspect.FrameInfo = inspect.stack()[1]
        module: Optional[object] = inspect.getmodule(frame[0])
        class_name: str = self.__class__.__name__
        file_path: str = (
            module.__file__ if module and hasattr(
                module, "__file__") else "unknown"
        )

        adapter: logging.LoggerAdapter = logging.LoggerAdapter(
            logger, {"app_name": f"{class_name} | {file_path}"}
        )
        return adapter

    # Default success messages based on HTTP method
    success_message: Dict = {
        "GET": {"title": "Success Message", "description": "Successfully fetched"},
        "POST": {"title": "Success Message", "description": "Successfully created"},
        "PUT": {"title": "Success Message", "description": "Successfully updated"},
        "DELETE": {"title": "Success Message", "description": "Successfully deleted"},
    }

    # Default exception message
    exception_message: Dict = {
        "title": "Exception",
        "description": "Internal Server Error",
    }

    def get_params(self) -> Dict:
        """
        Safely retrieves query parameters from the request.

        Returns:
            Dict: A dictionary of query parameters from the request.
        """
        try:
            params: dict = self.request.GET.dict()
        except Exception:
            params: dict = self.request.GET
        return params

    def get_queryset(self) -> QuerySet[Model]:
        """
        Returns the queryset to operate on.

        Returns:
            QuerySet[Model]: The queryset with all objects.
        """
        return self.queryset.all()

    def get_success_message(self) -> Optional[Dict]:
        """
        Returns a success message based on the HTTP request method.

        Returns:
            Optional[Dict]: The success message dictionary, if found.
        """
        return self.success_message.get(self.request.method)

    def custom_handle_exception(self, e: Exception) -> Response:
        """
        Logs an exception and returns a standardized error response.

        Args:
            e (Exception): The exception instance that was raised.

        Returns:
            Response: DRF Response object with error details and status code 400.
        """
        self.get_logger().info(
            f"{type(self).__name__} Method {self.request.method} API Exception, {str(e)}"
        )
        return Response(
            {"message": self.exception_message, "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def add_values_to_context(self):
        """
        if any extra values are required, they can 
        be explicitly added to context
        """
        return {}

    def set_context_data(self) -> Dict:
        """
        Constructs context data from the request and view kwargs.

        Returns:
            Dict: Context dictionary containing request and additional kwargs.
        """
        context: Dict = {
            "request": self.request,
            **self.kwargs,
            **self.add_values_to_context(),
        }
        return context

    def validation_response(self, validated_data: Dict) -> Response:
        """
        Returns a validation error response.

        Args:
            validated_data (Dict): The dictionary containing an 'error_message' key.

        Returns:
            Response: DRF Response with error message and status code 400.
        """
        return Response(
            {
                "message": validated_data.get("error_message"),
                "results": validated_data.get("field_errors", {}),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def success_response(self, validated_data: Union[List, Dict]) -> Response:
        """
        Returns a success response with validated data.

        Args:
            validated_data (Union[List, Dict]): The response payload data.

        Returns:
            Response: DRF Response with success message and results.
        """
        # self.get_logger().info("validated_data" + str(validated_data))
        return Response(
            {"message": self.get_success_message(), "results": validated_data}
        )

    def extract_error(self, serializer_error):
        error_dict: Dict = {}
        if isinstance(serializer_error, dict):
            for field_error in serializer_error.keys():
                error_dict[field_error] = serializer_error[field_error][0]

        return error_dict

    def check_custom_permission(self) -> Dict:
        return {}
