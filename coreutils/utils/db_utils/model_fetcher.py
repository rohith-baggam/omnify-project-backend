from typing import List

from django.apps import apps
from django.db.models import Model

from coreutils.utils.db_utils.get_custom_apps import GetCustomApps


class GetModels:
    """
    A utility class to retrieve all Django models from specified custom apps.
    """

    # ? Initialize with all available custom apps by default
    custom_apps: List[str] = GetCustomApps().get_custom_apps()

    def __init__(self, custom_apps: List[str] = [], filtered_apps: List[str] = []):
        """
        Initializes the class with either a predefined filtered list of apps
        or dynamically processes a provided list of custom apps.

        Args:
            custom_apps (List[str], optional): A list of full app names. Defaults to an empty list.
            filtered_apps (List[str], optional): A predefined filtered list of app names. Defaults to an empty list.
        """
        if filtered_apps:
            self.custom_apps = filtered_apps  # ? Use the provided filtered app list
        if custom_apps:
            # ? Process and extract the final app names from the given custom apps
            custom_app_instance = GetCustomApps(custom_apps)
            self.custom_apps = custom_app_instance.get_custom_apps()

    def get_custom_apps_models(self) -> List[Model]:
        """
        Retrieves all Django models from the specified custom apps.

        Returns:
            List[Model]: A list containing all models from the specified apps.
        """
        custom_models: List[Model] = []  # Store retrieved models

        for app in self.custom_apps:
            # ? Fetch all models from the app configuration and append them to the list

            app_models: List[Model] = apps.get_app_config(app).get_models()

            custom_models.extend(app_models)

        return custom_models
