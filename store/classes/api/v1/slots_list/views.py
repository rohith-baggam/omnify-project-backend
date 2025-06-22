from .serializers import ClassListModelSerializer
from store.classes.models import ClassAssignedInstructorModel
from coreutils.utils.generics.views.generic_views import CoreGenericListAPIView
from rest_framework import generics
from userauth.api.v1.utils.constants import USER_REGISTERED_SUCCESS_MESSAGE


class ClassListModelAPIView(CoreGenericListAPIView, generics.ListAPIView):
    queryset = ClassAssignedInstructorModel.objects.all()
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    success_message = USER_REGISTERED_SUCCESS_MESSAGE

    def get_serializer_class(self):
        serializer_class = {
            "GET": ClassListModelSerializer,
        }
        return serializer_class.get(self.request.method)
