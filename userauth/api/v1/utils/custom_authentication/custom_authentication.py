from rest_framework_jwt.authentication import (
    JSONWebTokenAuthentication,
    get_authorization_header,
)
import logging
from core.settings import logger
from rest_framework.request import Request
from typing import List
from userauth.api.v1.utils.custom_authentication.validations import (
    CustomAuthenticationValidator,
)
from rest_framework import exceptions


class CustomAuthentication(JSONWebTokenAuthentication):
    """
    Custom Authentication Class for User's
    """

    logger = logging.LoggerAdapter(logger, {"app_name": "CustomAuthentication"})

    www_authenticate_realm: str = "api"

    def get_token_from_request(self, request: Request):

        auth: List = get_authorization_header(request).split()
        custom_validator: CustomAuthenticationValidator = CustomAuthenticationValidator(
            request=request
        )
        validator: str = custom_validator.validator()

        if validator:
            raise exceptions.AuthenticationFailed(validator)

        return auth[1]
