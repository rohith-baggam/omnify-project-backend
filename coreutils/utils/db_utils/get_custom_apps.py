from typing import List

from core.settings import CUSTOM_APPS


class GetCustomApps:
    custom_apps: List = CUSTOM_APPS

    def __init__(self, custom_apps: List = []):
        if custom_apps:
            self.custom_apps = custom_apps

    def refactor_apps(self, app_names: str, app: List[str]):
        """
        Extracts and appends the final app name from a potentially nested app structure.

        If the app name is a sub-app (e.g., "user_config.user_auth"),
        it extracts only the final part ("user_auth") and appends it to the list.
        Otherwise, it appends the app name as is.

        Args:
            app_names (str): The app name, which may be a sub-app in a dotted path.
            app (list): The list to which the extracted app name is appended.
        """
        if "." in app_names:
            # ? Extracts the last part of the app name
            app_name: str = app_names.split(".")[-1]
            app.append(app_name)
        else:
            app.append(app_names)

    def refactor_command(self, custom_apps: List[str]) -> List[str]:
        """
        Processes a list of custom apps and extracts only the final app names.

        This ensures that `makemigrations` is run only for the relevant Django apps.

        Args:
            custom_apps (list): List of full app names (may include sub-apps).

        Returns:
            list: A list of extracted app names.
        """
        app: List = []
        for app_names in custom_apps:
            self.refactor_apps(app_names=app_names, app=app)
        return app

    def get_custom_apps(self) -> List[str]:
        """
        Retrieves the list of custom apps and refactors their names.

        This method processes the custom apps stored in the class and extracts only
        their final names, ensuring they are properly formatted for use in Django commands.

        Returns:
            list: A list containing the final app names (without nested module paths).
        """
        return self.refactor_command(custom_apps=self.custom_apps)
