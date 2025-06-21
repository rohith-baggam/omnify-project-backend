from coreutils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
import logging
from typing import Dict
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from core.settings import logger
from userauth.api.v1.utils.user_login_utils import (
    ValidateUserLogin,
)
from coreutils.utils.generics.serializers.mixins import (
    CoreGenericSerializerMixin,
)
from userauth.api.v1.utils.handlers.register_handler import UserAuthRegisterHandler

# Logger setup with application context
logger: logging.LoggerAdapter = logging.LoggerAdapter(
    logger, {"app_name": "user_config.user_auth.api.v1.authentication.serializers.py"}
)


class UserLoginWebTokenSerializer(JSONWebTokenSerializer):
    """
    Serializer for handling user login authentication with JWT tokens.
    It validates user credentials, ensures proper authentication, and
    returns a JWT token upon successful login.
    """

    # Logger specific to this serializer
    logger: logging.LoggerAdapter = logging.LoggerAdapter(
        logger, {"app_name": "UserLoginWebTokenSerializer"}
    )

    # Fields required for user authentication
    email: str = serializers.EmailField(required=True, help_text="User email address.")
    password: str = serializers.CharField(
        required=True, write_only=True, help_text="User password."
    )
    re_login: bool = serializers.BooleanField(
        default=False, help_text="Flag to allow re-login if multi-login is disabled."
    )

    def validate(self, data: Dict) -> Dict:
        """
        Validate user login credentials and generate a JWT token if successful.

        Args:
            data (dict): A dictionary containing user-provided email, password, and re-login flag.

        Returns:
            dict: A dictionary containing the authenticated user instance and JWT token.

        Raises:
            serializers.ValidationError: If authentication fails due to incorrect credentials
                                         or multiple active logins (if restricted).
        """
        # ? Initialize user login validation utility
        validate_user_login: ValidateUserLogin = ValidateUserLogin(
            email=data["email"], password=data["password"], re_login=data["re_login"]
        )

        # ? Validate user credentials and check for errors
        validation_errors: str = validate_user_login.validate_login()

        # ? Raise an error if validation fails
        if validation_errors:
            raise serializers.ValidationError(validation_errors)

        # ? Generate JWT token after successful validation
        jwt_token: str = validate_user_login.set_jwt_token()

        # ? Return authenticated user and token
        return {"user": validate_user_login.user_instance, "token": jwt_token}


class UserAuthRegisterSerializer(CoreGenericSerializerMixin, serializers.Serializer):
    handler_class = UserAuthRegisterHandler
    queryset = get_user_model().objects.all()

    # ? Fields for updating
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
