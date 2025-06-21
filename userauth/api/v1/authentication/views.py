from .serializers import UserAuthRegisterSerializer
from django.contrib.auth import get_user_model
from coreutils.utils.generics.views.generic_views import CoreGenericPostAPIView
from rest_framework import generics
from userauth.api.v1.utils.constants import USER_REGISTERED_SUCCESS_MESSAGE


class UserAuthRegisterAPIView(
    CoreGenericPostAPIView,
    generics.GenericAPIView,
):
    queryset = get_user_model().objects.all()
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    success_message = USER_REGISTERED_SUCCESS_MESSAGE

    def get_serializer_class(self):
        serializer_class = {
            "POST": UserAuthRegisterSerializer,
        }
        return serializer_class.get(self.request.method)
