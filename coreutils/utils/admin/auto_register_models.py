from typing import List

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.db.models import Model


from coreutils.utils.generics.generic_models import CoreGenericModel
from coreutils.utils.db_utils.model_fetcher import GetModels

# ? Fetching auto-registration settings from Django settings
AUTO_REGISTER_MODEL_APPS: List = getattr(settings, "AUTO_REGISTER_MODEL_APPS", [])
AUTO_REGISTER_MODELS: bool = getattr(settings, "AUTO_REGISTER_MODELS", False)
CUSTOM_APPS: List = getattr(settings, "CUSTOM_APPS", [])


class AutoRegisterModel:
    """
    Class to automatically register Django models in the admin panel.
    It dynamically discovers models from specified applications and
    registers them with dynamically created ModelAdmin classes.
    """

    custom_apps: List = CUSTOM_APPS  # ? Default list of custom apps

    def __init__(self, custom_apps: List[str] = []):
        """
        Initialize AutoRegisterModel instance.

        Args:
            custom_apps (List[str], optional): List of custom app names.
                                               Defaults to an empty list.
        """
        if custom_apps:
            self.custom_apps = custom_apps  # ? Override default apps with provided list
        if AUTO_REGISTER_MODEL_APPS:
            # ? Use auto-register settings if available
            self.custom_apps = AUTO_REGISTER_MODEL_APPS

    def get_registered_apps(self) -> List[str]:
        """
        Retrieve the list of applications whose models should be auto-registered.

        Returns:
            List[str]: A list of application names.
        """
        if AUTO_REGISTER_MODELS:
            return self.custom_apps
        return []

    def get_registered_app_models(self) -> List[Model]:
        """
        Fetch all models from the registered applications.

        Returns:
            List[Model]: A list of Django model classes.
        """
        get_model_instance = GetModels(self.get_registered_apps())
        return get_model_instance.get_custom_apps_models()

    def get_core_generic_field_names(self):
        """
        List of fields inherited from CoreGenericModel
        """
        return [field.name for field in CoreGenericModel._meta.get_fields()]

    def register_models(self):
        """
        Register models dynamically in the Django admin site.
        It creates a dynamic ModelAdmin class with fields auto-configured
        based on model attributes.
        """
        models_list: List[Model] = self.get_registered_app_models()

        for model in models_list:

            class DynamicAdmin(admin.ModelAdmin):
                """
                Dynamically generated ModelAdmin class with fields filtered based on type.
                This class automatically configures the `list_display` and `search_fields`
                attributes for the admin panel.
                """

                # ? Define list_display for admin panel (exclude inherited fields and primary keys)
                list_display: List = [
                    field.name
                    for field in model._meta.fields
                    if field.name not in self.get_core_generic_field_names()
                    and not field.primary_key
                    and not isinstance(field, (models.TextField, models.JSONField))
                ]

                # ? Ensure primary keys are displayed first in the admin panel
                list_display: List = [
                    *[field.name for field in model._meta.fields if field.primary_key],
                    *list_display,
                ]

                # ? Define search fields (Only CharField & UUIDField, excluding inherited fields)
                search_fields: List = [
                    field.name
                    for field in model._meta.fields
                    if isinstance(field, (models.CharField, models.UUIDField))
                    and field.name not in self.get_core_generic_field_names()
                ]

            # ? Register model with dynamically generated ModelAdmin class
            admin.site.register(model, DynamicAdmin)
