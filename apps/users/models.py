from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.db import models

from apps.users.manager import UserManager
from core.enum.validate import ValidateUser as valid
from core.models import CoreModel


class ProfileModel(CoreModel):
    class Meta:
        db_table = "profile_users"

    name = models.CharField(
        max_length=25, validators=[validators.RegexValidator(*valid.NAME_SURNAME.value)]
    )
    surname = models.CharField(
        max_length=25, validators=[validators.RegexValidator(*valid.NAME_SURNAME.value)]
    )
    bio = models.TextField()
    age = models.IntegerField(
        validators=[validators.MinValueValidator(18), validators.MaxValueValidator(90)]
    )
    avatar = models.ImageField(upload_to="image/", blank=True)


class TypeAccount(CoreModel):
    class Meta:
        db_table = "type_acount_user"

    is_seller = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    expire_premium = models.DateTimeField(
        blank=True,
        null=True,
        validators=[
            validators.MinValueValidator(datetime.now() + timedelta(days=1)),
            validators.MaxValueValidator(
                datetime.now() + timedelta(days=90)
            ),  # del this
        ],
    )


class UserModel(AbstractBaseUser, PermissionsMixin, CoreModel):
    class Meta:
        db_table = "auth_users"

    email = models.EmailField(unique=True)
    password = models.CharField(
        max_length=128, validators=[validators.RegexValidator(*valid.PASSWORD.value)]
    )

    # type_account
    is_active = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    # role_standard
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # profile
    profile = models.OneToOneField(
        ProfileModel, on_delete=models.SET_NULL, null=True, related_name="user"
    )
    # account
    account = models.OneToOneField(
        TypeAccount, on_delete=models.SET_NULL, null=True, related_name="user"
    )

    # settings model
    USERNAME_FIELD = "email"
    objects = UserManager()
