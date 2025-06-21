import uuid

from django.apps import apps
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models, transaction

from coreutils.utils.generics.generic_models import CoreGenericModel


# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Object Manager for UserModel
    """

    def create_user(
        self, email: str, password: str = None, **extra_fields
    ) -> AbstractBaseUser:
        """
        This is a manager method to create a user
        """
        with transaction.atomic():
            if not email:
                raise ValueError("Email is required")

            email: str = self.normalize_email(email)
            user: AbstractBaseUser = self.model(email=email, **extra_fields)

            if password:
                user.set_password(password)

            user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str) -> AbstractBaseUser:
        """
        This is a manager method to create a superuser
        """
        extra_fields: dict = {
            "is_superuser": True,
            "is_active": True,
            "is_approved": True,
            "is_verified": True,
            "is_staff": True,
        }

        return self.create_user(email=email, password=password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="USER_AUTH_ID",
        editable=False,
    )

    username = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column="USERNAME",
    )
    email = models.EmailField(
        max_length=100,
        db_column="EMAIL",
        unique=True,
    )

    # ? Permissions
    # ? Default django abstract Permissions
    is_staff = models.BooleanField(
        default=False,
        db_column="IS_STAFF",
    )
    is_active = models.BooleanField(
        default=False,
        db_column="IS_ACTIVE",
    )
    is_superuser = models.BooleanField(
        default=False,
        db_column="IS_SUPERUSER",
    )
    # ? custom permissions
    is_verified = models.BooleanField(
        default=False,
        db_column="IS_VERIFIED",
    )
    is_approved = models.BooleanField(
        default=False,
        db_column="IS_APPROVED",
    )

    # ? project permissions
    is_client = models.BooleanField(
        default=False,
        db_column="IS_CLIENT"
    )
    is_instructor = models.BooleanField(
        default=False,
        db_column="IS_INSTRUCTOR"
    )

    # ? Custom Fields

    custom_password = models.TextField(
        null=True,
        blank=True,
        db_column="CUSTOM_PASSWORD",
    )

    last_login = models.DateTimeField(
        null=True,
        blank=True,
        db_column="LAST_LOGIN",
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        db_column="CREATED_DATE",
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        db_column="UPDATED_DATE",
    )

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = "USER_TABLE"


class BlackListTokenModel(CoreGenericModel):
    id = models.UUIDField(
        db_column="BLACKLIST_TOKEN_ID",
        default=uuid.uuid1,
        unique=True,
        primary_key=True,
        editable=False,
    )
    token = models.TextField(db_column="JWT_TOKEN")
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="BlackListTokenModel_user",
        db_column="USER_ID",
    )
    is_login = models.BooleanField(
        default=False,
        db_column="IS_LOGIN",
    )
    is_delete = models.BooleanField(
        default=False,
        db_column="IS_DELETE",
    )

    class Meta:
        db_table = "USER_BLACK_LIST_TOKEN_TABLE"


class LoginAnalyticsModel(CoreGenericModel):
    id = models.UUIDField(
        db_column="USER_LOGIN_ANALYTICS_ID",
        default=uuid.uuid1,
        unique=True,
        primary_key=True,
        editable=False,
    )
    ip_address = models.CharField(
        max_length=255,
        db_column="IP_ADDRESS",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="LoginAnalyticsModel_user",
        db_column="USER_ID",
    )
    login_count = models.IntegerField(
        default=0,
        db_column="LOGIN_COUNT",
    )
    device_name = models.CharField(max_length=255, db_column="DEVICE_NAME")
    token = models.TextField(
        null=True,
        blank=True,
        db_column="TOKEN",
    )

    class Meta:
        db_table = "USER_LOGIN_ANALYTICS_TABLE"
