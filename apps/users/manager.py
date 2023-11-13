import os
from datetime import datetime, timedelta

import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from django.http import Http404

from config.settings import LANGUAGE_CODE
from core.exceptions.jwt_exception import BlockException
from core.system_message_errors.message_user import (
    UserCreateMessageValidateDefaultFields as msg,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Fields email must be required")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_admin(self, email, password, **kwargs):
        kwargs.setdefault("is_superuser", False)
        staff = msg("Admin", **kwargs)
        kwargs = staff.validate_base_fields()
        if not kwargs.get("is_superuser"):
            raise ValueError(staff.error_message_superuser(status=False))

        user = self.create_user(email, password, **kwargs)
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_superuser", True)
        superuser = msg("Superuser", **kwargs)
        kwargs = superuser.validate_base_fields()
        if not kwargs.get("is_superuser"):
            raise ValueError(superuser.error_message_superuser(status=True))

        user = self.create_user(email, password, **kwargs)
        return user

    def block_user(self, user):
        user = get_user_model().objects.get(pk=user.pk)
        if user and not user.is_superuser and not user.is_staff and not user.is_block:
            user.is_block = True
            user.save()
            return user
        else:
            raise Http404

    def unblock_user(self, user):
        user = get_user_model().objects.get(pk=user.pk)
        if user and user.is_block:
            user.is_block = False
            user.save()
            return user
        else:
            raise Http404

    def add_premium(self, user, time: dict):  # days=1, days=15, days=30, days=90
        timezone = pytz.timezone(os.environ.get("TIMEZONE"))
        user = get_user_model().objects.get(pk=user.pk)
        if user and user.account and not user.is_block:
            account = user.account
            account.is_premium = True
            account.expire_premium = timezone.localize(
                datetime.now() + timedelta(days=int(time.get("days")[0]))
            )
            account.save()
            return user
        else:
            raise Http404 if not user.is_block else BlockException

    def delete_premium(self, user):
        user = get_user_model().objects.get(pk=user.pk)
        if user and user.account:
            if user.account.is_premium:
                user.account.is_premium = False
                user.save()
                return user
        raise Http404
