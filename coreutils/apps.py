from django.apps import AppConfig


class CoreutilsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "coreutils"

    def ready(self):
        from django.conf import settings

        if getattr(settings, "AUTO_REGISTER_MODELS", False):
            from coreutils.utils.admin.auto_register_models import AutoRegisterModel

            AutoRegisterModel().register_models()
