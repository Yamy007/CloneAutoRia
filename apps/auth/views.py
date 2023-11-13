from rest_framework import exceptions
from rest_framework.fields import Field
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serializers import UserSerializer
from core.service.jwt_service import ActivateToken, JWTService


def default_user_authentication_rule(user):
    print(user)
    if user:
        if user.is_block:
            raise exceptions.AuthenticationFailed({"detail": "Block account"})
    return user is not None and user.is_active and not user.is_block


class ActivateTokenView(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        token = kwargs["token"]
        user = JWTService.validate_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializers = UserSerializer(user)
        return Response(serializers.data, 200)
