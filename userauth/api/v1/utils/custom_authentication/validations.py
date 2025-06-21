from rest_framework.request import Request
from rest_framework_jwt.authentication import (
    get_authorization_header,
)
from typing import List, ByteString, Union, Callable
from rest_framework_jwt.settings import api_settings
from django.utils.encoding import smart_str
import logging
from core.settings import logger
from django.conf import settings
from userauth.models import BlackListTokenModel
from coreutils.utils.jwt_token_utils import JwtTokenUtils

DISABLE_MULTI_LOGIN: List = getattr(settings, "DISABLE_MULTI_LOGIN", True)


class ExtractAuthenticationDetails:
    request: Request
    jwt_token: str
    auth_headers: List[ByteString]

    def __init__(self, request: Request):
        self.request = request
        self.auth_headers = self.set_auth_headers()
        self.jwt_token = self.set_jwt_token()

    def set_auth_headers(self) -> List[ByteString]:
        self.auth_headers: List[ByteString] = get_authorization_header(
            self.request
        ).split()
        return self.auth_headers

    def set_jwt_token(self) -> Union[str, None]:
        try:
            self.jwt_token: str = self.auth_headers[1].decode("utf-8")
        except:
            self.jwt_token: None = None
        return self.jwt_token

    def get_auth_header_prefix(self) -> str:
        try:
            auth_header_prefix: str = api_settings.JWT_AUTH_HEADER_PREFIX.lower()
        except:
            auth_header_prefix: str = "Bearer"
        return auth_header_prefix


class CustomAuthenticationValidator:
    request: Request
    authentication_details: ExtractAuthenticationDetails
    DISABLE_MULTI_LOGIN: bool = getattr(settings, "DISABLE_MULTI_LOGIN", None)
    logger = logging.LoggerAdapter(
        logger, {"app_name": "CustomAuthenticationValidator"}
    )

    def __init__(self, request: Request):
        self.request = request
        self.authentication_details = ExtractAuthenticationDetails(
            request=request)

    def auth_headers_length_validator(self) -> Union[str, None]:
        if not self.authentication_details.jwt_token:
            error_message: str = "Jwt Token is missing"
            self.logger.error(error_message)
            return error_message
        if not self.authentication_details.auth_headers:
            error_message: str = "returning none as token != auth header prefix"
            self.logger.error(error_message)
            return error_message
        if len(self.authentication_details.auth_headers) == 1:
            error_message: str = "returning none as token != auth header prefix"
            self.logger.error(error_message)
            return error_message
        if len(self.authentication_details.auth_headers) != 2:
            error_message: str = "returning none as token != auth header prefix"
            self.logger.error(error_message)
            return error_message
        if (
            smart_str(self.authentication_details.auth_headers[0].lower())
            != self.authentication_details.get_auth_header_prefix()
        ):
            error_message: str = "returning none as token != auth header prefix"
            self.logger.error(error_message)
            return error_message

    def black_list_token_validator(self) -> Union[str, None]:
        if not DISABLE_MULTI_LOGIN:
            return

        blacklist_token_queryset = BlackListTokenModel.objects.filter(
            token=self.authentication_details.jwt_token, is_login=True
        )
        if not blacklist_token_queryset.exists():
            error_message: str = "Signature has expired"
            self.logger.error(error_message)
            return error_message

    def token_validator(self) -> Union[str, None]:
        jwt_token_util: JwtTokenUtils = JwtTokenUtils(
            jwt_token=self.authentication_details.jwt_token
        )
        print("jwt_token_util.is_token_expired()",
              jwt_token_util.is_token_expired())
        if jwt_token_util.is_token_expired():
            return "jwt token expired"

    def validator(self) -> str:
        validate_methods: List[Callable] = [
            self.auth_headers_length_validator,
            self.token_validator,
            self.black_list_token_validator,
        ]
        for method in validate_methods:
            error_message: Union[str, None] = method()
            if error_message:
                return error_message
