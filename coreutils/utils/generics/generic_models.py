from django.db import models


class CoreGenericModel(models.Model):
    """
    All models in the project should inherit from CoreGenericModel, an abstract base model that centralizes common fields and logic. This allows for global control over all models in the application.
    """

    core_generic_created_at = models.DateTimeField(
        auto_now_add=True, null=True, db_column="CORE_GENERIC_CREATED_AT"
    )
    core_generic_updated_at = models.DateTimeField(
        auto_now=True, null=True, db_column="CORE_GENERIC_LAST_UPDATED_AT"
    )
    core_generic_created_by = models.CharField(
        max_length=100, null=True, blank=True, db_column="CORE_GENERIC_CREATED_BY"
    )
    core_generic_updated_by = models.CharField(
        max_length=100, null=True, blank=True, db_column="CORE_GENERIC_UPDATED_BY"
    )

    class Meta:
        abstract = True
