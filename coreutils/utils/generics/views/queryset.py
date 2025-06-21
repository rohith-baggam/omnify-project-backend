from django.db.models import Model
from django.db.models.query import QuerySet
from typing import Dict, Any, Union
from coreutils.utils.generics.views.core_generic_utils import CoreGenericUtils


class CoreGenericQueryset(CoreGenericUtils):
    """
    Utility class that extends CoreGenericUtils to provide
    ordering and queryset handling for list-based views.
    """

    # ? Query parameter name to specify ordering
    ordering_param_name: str = "ordering"
    queryset: QuerySet  # ? Should be overridden by subclass or view
    default_ordering_field: str = "-core_generic_created_at"  # ? Default ordering
    rename_sorting_params: dict = {}

    def get_ordering_dict(self) -> Union[str, None]:
        """
        Retrieves the ordering field from the request parameters.

        Returns:
            Union[str, None]: The ordering field as a string. Defaults to 'default_ordering_field'
                              if not provided in query params.
        """
        params: Dict = self.get_params()
        if params.get(self.ordering_param_name):
            return self.rename_sorting_params.get(
                params[self.ordering_param_name], params[self.ordering_param_name]
            )
        return self.default_ordering_field

    def get_queryset_order_by(self) -> QuerySet:
        """
        Applies ordering to the queryset.

        Returns:
            QuerySet: Ordered queryset based on ordering field.
        """
        return self.queryset.order_by(self.get_ordering_dict())

    def get_queryset(self) -> QuerySet:
        """
        Returns the ordered queryset. Meant to be overridden if additional filtering is needed.

        Returns:
            QuerySet: Ordered queryset.
        """
        return self.get_queryset_order_by()

    def get_filtered_queryset(self) -> QuerySet:
        """
        Returns the filtered queryset. Currently defaults to ordered queryset.
        Can be overridden to apply custom filtering.

        Returns:
            QuerySet: Filtered (or just ordered) queryset.
        """
        return self.get_queryset()

    def get_paginate_queryset(self) -> QuerySet[Model]:
        """
        Paginates the filtered and ordered queryset using DRF's pagination mechanism.

        Returns:
            QuerySet[Model]: Paginated queryset.
        """
        return self.paginate_queryset(
            self.filter_queryset(self.get_queryset_order_by())
        )


class CoreGenericQuerysetInstance(CoreGenericUtils):
    """
    Utility class that extends CoreGenericUtils to provide
    single object retrieval based on a primary key from request data.
    """

    # ? Can be PARAMS (query), BODY (request.data), or KWARGS (URL kwargs)
    pk_scope: str = "PARAMS"
    pk_field: str = "id"  # ? Default field to lookup by

    def get_pk_value(self, pk_field: str) -> Any:
        """
        Extracts the primary key value from the appropriate scope.

        Args:
            pk_field (str): The field name to use for primary key lookup.

        Raises:
            Exception: If the scope is undefined or incorrect.

        Returns:
            Any: The value of the primary key.
        """
        if self.pk_scope == "PARAMS":
            pk_value: Any = self.get_params().get(pk_field)
        elif self.pk_scope == "BODY":
            pk_value: Any = self.request.data.get(pk_field)
        elif self.pk_scope == "KWARGS":
            pk_value: Any = self.kwargs.get(pk_field)
        else:
            raise Exception("pk_scope is not defined or Incorrect scope")
        return pk_value

    def get_filterset_for_pk(self, pk_field: str = "id") -> Dict:
        """
        Constructs a filter dictionary using the primary key.

        Args:
            pk_field (str): The field name to filter by. Defaults to 'id'.

        Returns:
            Dict: Filter dictionary like {'id': 123}
        """
        if not pk_field:
            pk_field: str = self.pk_field

        filter_set: Dict = {pk_field: self.get_pk_value(pk_field=pk_field)}
        return filter_set

    def get_object(self) -> Model:
        """
        Retrieves a single model instance using the primary key filter.

        Returns:
            Model: A single model instance matching the filter.
        """
        return self.get_queryset().get(**self.get_filterset_for_pk())

    def get_object_pk_validation(self) -> str | None:
        if self.many or self.skip_validation:
            return
        if not self.get_pk_value(pk_field=self.pk_field):
            return {
                "title": f"Id validation",
                "description": f"Please pass a valid ID in {str(self.pk_scope).lower()}",
            }
        if not self.queryset.filter(**self.get_filterset_for_pk()).exists():
            return self.INCORRECT_ID_EXCEPTION
