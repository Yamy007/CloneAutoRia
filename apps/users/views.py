import os

import requests
from django.http import Http404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.filter import UserFilter
from apps.users.serializers import (
    DetailPremiumSerializer,
    ProfileSerializer,
    TimeSerializers,
    UserModelFunction,
    UserSerializer,
    UserUpdateSerializer,
)
from core.models import DetailPremiumModel
from core.permissions import IsAdmin, IsNotBlock, IsSuperUser


class CreateUser(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class CreateUserAsSeller(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data, context={"is_seller": True})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateAdminUser(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)

    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data, context={"is_staff": True})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateUserPermissions(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsSuperUser,)
    http_method_names = ("patch",)

    def get_queryset(self):
        return UserModelFunction.objects.exclude(pk=self.request.user.pk)


class UpdateProfileUser(UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsNotBlock,)
    http_method_names = ("patch",)

    def get_object(self):
        user = UserModelFunction.objects.filter(
            profile__isnull=False, pk=self.request.user.pk
        ).first()
        if user:
            return user.profile
        else:
            raise Http404


class UpdateProfileUserById(UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAdmin,)
    http_method_names = ("patch",)

    def get_object(self):
        user = UserModelFunction.objects.filter(pk=self.kwargs.get("pk")).first()
        if user:
            return user.profile
        else:
            raise Http404


class AllUsers(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    queryset = UserModelFunction.objects.all()
    filterset_class = UserFilter


class GetUserById(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    queryset = UserModelFunction.objects.all()


class GetMeUser(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsNotBlock,)

    def get_object(self):
        return UserModelFunction.objects.get(pk=self.request.user.pk)


class BlockedUser(GenericAPIView):
    permission_classes = (IsAdmin,)
    queryset = UserModelFunction.objects.all()

    def post(self, *args, **kwargs):
        user = self.get_object()
        user = UserModelFunction.objects.block_user(user)
        return Response("Success", status=status.HTTP_200_OK)


class UnBlockedUser(GenericAPIView):
    permission_classes = (IsAdmin,)
    queryset = UserModelFunction.objects.all()

    def post(self, *args, **kwargs):
        user = self.get_object()
        user = UserModelFunction.objects.unblock_user(user)
        return Response("Success", status=status.HTTP_200_OK)


class GetPremiumAccount(GenericAPIView):
    permission_classes = (IsAdmin,)
    queryset = UserModelFunction.objects.exclude(account__isnull=True)

    def post(self, *args, **kwargs):
        user = self.get_object()
        data = self.request.data
        serializers = TimeSerializers(data=data)
        serializers.is_valid(raise_exception=True)
        user = UserModelFunction.objects.add_premium(user=user, time=data)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class DeletePremiumAccount(GenericAPIView):
    permission_classes = (IsAdmin,)
    queryset = UserModelFunction.objects.exclude(account__isnull=True)

    def post(self, *args, **kwargs):
        user = self.get_object()
        user = UserModelFunction.objects.delete_premium(user)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class GetTimePremium(ListCreateAPIView):
    permission_classes = (IsAdmin,)
    queryset = DetailPremiumModel.objects.all()
    serializer_class = DetailPremiumSerializer


class SetDestroyTimePremium(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    queryset = DetailPremiumModel.objects.all()
    serializer_class = DetailPremiumSerializer
    http_method_names = ("patch", "put", "delete")
