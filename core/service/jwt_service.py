from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import BlacklistMixin, Token

from core.enum.token import TokenEnum
from core.exceptions.jwt_exception import JWTException


class ActivateToken(BlacklistMixin, Token):
    token_type = TokenEnum.ACTIVATE.token_type
    lifetime = TokenEnum.ACTIVATE.life_time


class JWTService:
    @staticmethod
    def create_token(user, token_class):
        return token_class.for_user(user)

    @staticmethod
    def validate_token(token, token_class):
        try:
            res = token_class(token)
            res.check_blacklist()
        except Exception:
            raise JWTException
        res.blacklist()
        user_id = res.payload.get("user_id")
        return get_object_or_404(get_user_model(), pk=user_id)
