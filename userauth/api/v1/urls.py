from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebTokenView
from userauth.api.v1.authentication.serializers import (
    UserLoginWebTokenSerializer
)

from userauth.api.v1.authentication.views import (
    UserAuthRegisterAPIView
)

urlpatterns = [
    path(
        "user-login-api/",
        ObtainJSONWebTokenView.as_view(
            serializer_class=UserLoginWebTokenSerializer),
        name="ObtainJSONWebTokenView",
    ),
    path(
        "user-register-api/",
        UserAuthRegisterAPIView.as_view(),
        name="UserAuthRegisterAPIView"
    )

    # UserAuthRegisterAPIView
]
