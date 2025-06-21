from django.db import transaction
from coreutils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from userauth.models import UserModel


class UserAuthRegisterHandler(CoreGenericBaseHandler):
    def validate(self):
        if self.queryset.filter(email=self.data["email"]).exists():
            return self.set_error_message(
                error_message={
                    "title": "Failed to update.",
                    "description": "An account with this email already exists.",
                },
                key="email",
            )
        return

    def create(self):
        try:
            with transaction.atomic():
                instance: UserModel = self.queryset.create(
                    email=self.data["email"], username=self.data["username"]
                )
                instance.set_password(raw_password=self.data["password"])
                instance.save()
        except Exception as e:
            raise Exception(f"Error while updating user details : {str(e)}")
