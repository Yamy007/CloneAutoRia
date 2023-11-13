import django.db
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.users.models import ProfileModel, TypeAccount
from core.models import DetailPremiumModel
from core.service.email_service import EmailService

UserModelFunction = get_user_model()


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ["id", "name", "surname", "bio", "age", "avatar"]
        read_only_fields = ("id",)


class AccountSerializer(ModelSerializer):
    class Meta:
        model = TypeAccount
        fields = ["id", "is_seller", "is_premium", "expire_premium"]
        read_only_fields = ("id",)

    def validate(self, attrs):
        if not attrs.get("expire_premium") and attrs.get("is_premium"):
            raise serializers.ValidationError("You must have expire_premium ")
        else:
            return attrs


class UserUpdateSerializer(ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    account = AccountSerializer(read_only=True)

    class Meta:
        model = UserModelFunction
        fields = (
            "id",
            "email",
            "is_block",
            "is_staff",
            "is_active",
            "last_login",
            "profile",
            "account",
        )
        read_only_fields = (
            "id",
            "email",
            "last_login",
            "profile",
            "account",
        )

    def validate(self, attrs):
        if attrs.get("is_staff") and attrs.get("is_block"):
            raise serializers.ValidationError("Staff cannot be block")
        return attrs


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()
    account = AccountSerializer(read_only=True)

    class Meta:
        model = UserModelFunction
        fields = (
            "id",
            "email",
            "password",
            "is_active",
            "is_block",
            "is_staff",
            "is_superuser",
            "profile",
            "account",
            "create_at",
            "update_at",
            "last_login",
        )
        read_only_fields = (
            "id",
            "is_active",
            "is_block",
            "is_staff",
            "is_superuser",
            "last_login",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    @atomic
    def create(self, validated_data):
        profile = validated_data.pop("profile")
        account = TypeAccount.objects.create(
            is_seller=bool(self.context.get("is_seller"))
        )
        profile = ProfileModel.objects.create(**profile)
        validated_data.setdefault("is_staff", bool(self.context.get("is_staff")))
        user = UserModelFunction.objects.create_user(
            **validated_data, profile=profile, account=account
        )
        EmailService.register_email(user) if not self.context.get("is_staff") else None
        return user


class ShortUserSerializer(ModelSerializer):
    account = AccountSerializer(read_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = UserModelFunction
        fields = ("id", "email", "account", "profile")


class TimeSerializers(serializers.Serializer):
    days = serializers.IntegerField()

    def validate(self, attrs):
        days = attrs.get("days")
        if DetailPremiumModel.objects.filter(days=days).exists():
            return attrs
        else:
            raise serializers.ValidationError(
                "You cant use this value for premium accounts"
            )


class DetailPremiumSerializer(ModelSerializer):
    class Meta:
        model = DetailPremiumModel
        fields = ["id", "days", "price"]


class UserShowSerializer(ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    account = AccountSerializer(read_only=True)

    class Meta:
        model = UserModelFunction
        fields = (
            "id",
            "email",
            "profile",
            "account",
        )
