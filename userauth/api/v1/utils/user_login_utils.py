from typing import Callable, Dict, Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.query import QuerySet
from rest_framework_jwt.settings import api_settings

from userauth.api.v1.utils.constants import (
    ACCOUNT_INACTIVE_ERROR_MESSAGE,
    BLACKLIST_TOKEN_ALREADY_EXISTS_ERROR_MESSAGE,
    INCORRECT_CREDENTIALS_ERROR_MESSAGE,
)
from userauth.models import BlackListTokenModel

# ? REST Framework JWT settings handlers
jwt_payload_handler: Dict = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler: Callable[[dict], str] = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler: Callable[[str], dict] = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload: Callable[[dict], str] = (
    api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
)


class ValidateUserLogin:
    """
    Handles user login validation, ensuring that credentials are correct
    and checking for active login tokens if multi-login is disabled.

    Constructor Attributes;
        email (str): User's email for authentication.
        password (str): User's password for authentication.
        re_login (bool): Indicates if the user is attempting to re-login.

    Attributes:
        DISABLE_MULTI_LOGIN (bool): Determines whether multiple logins per user are allowed.
        email (str): User's email for authentication.
        password (str): User's password for authentication.
        re_login (bool): Indicates if the user is attempting to re-login.
        user_instance (AbstractBaseUser): Stores the user instance after successful validation.
        jwt_token (str): JWT token generated for the user.
        payload (Dict): JWT payload containing user authentication details.

    """

    DISABLE_MULTI_LOGIN: bool = getattr(settings, "DISABLE_MULTI_LOGIN", None)

    email: str
    password: str
    re_login: bool
    user_instance: AbstractBaseUser
    jwt_token: str
    payload: Dict

    def __init__(self, email: str, password: str = None, re_login: bool = False):
        """
        Initializes the ValidateUserLogin class with user credentials.

        Args:
            email (str): User's email address.
            password (str, optional): User's password for authentication. Defaults to None.
            re_login (bool, optional): Indicates if the user is attempting to re-login. Defaults to False.
        """
        self.email: str = email
        self.password: str = password
        self.re_login: bool = re_login

    def is_blacklist_token_exists(self) -> bool:
        """
        Checks if the user already has an active blacklist token when multi-login is disabled.

        Returns:
            bool: True if an active token exists, otherwise False.
        """
        # ? Only check for a blacklist token if multi-login is disabled
        if self.DISABLE_MULTI_LOGIN:
            black_list_queryset: QuerySet[BlackListTokenModel] = (
                BlackListTokenModel.objects.filter(user__email=self.email)
            )
            return black_list_queryset.filter(is_login=True).exists()
        return False

    def validate_login(self) -> Union[str, None]:
        """
        Validates the user login credentials and checks for active sessions if re-login is not allowed.

        Returns:
            str: An error message if validation fails, otherwise None.
        """
        user_queryset: QuerySet[AbstractBaseUser] = get_user_model(
        ).objects.all()

        # ? Check if a user with the provided email exists
        if not user_queryset.filter(email=self.email).exists():
            return INCORRECT_CREDENTIALS_ERROR_MESSAGE

        user_instance: AbstractBaseUser = user_queryset.get(email=self.email)

        # ? Ensure the user account is active
        if not user_instance.is_active:
            return ACCOUNT_INACTIVE_ERROR_MESSAGE

        # ? Validate the provided password
        if not user_instance.check_password(raw_password=self.password):
            return INCORRECT_CREDENTIALS_ERROR_MESSAGE

        self.user_instance: AbstractBaseUser = user_instance

        # ? If multi-login is disabled, check for existing active login tokens
        if not self.re_login and self.is_blacklist_token_exists():
            return BLACKLIST_TOKEN_ALREADY_EXISTS_ERROR_MESSAGE

    def set_jwt_payload(self) -> Dict:
        """
        Generates the JWT payload for the authenticated user.

        Returns:
            Dict: The JWT payload containing user authentication details.
        """
        self.payload: Dict = jwt_payload_handler(self.user_instance)
        return self.payload

    def set_jwt_token(self) -> str:
        """
        Generates a JWT token for the authenticated user.

        Returns:
            str: The generated JWT token.
        """
        self.jwt_token: str = jwt_encode_handler(self.set_jwt_payload())
        return self.jwt_token
