import django.db
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.advertisements.models import (
    AdvertisementModel,
    AlbumCarModel,
    CarModel,
    DetailCarModel,
    StaticAdvertisementModel,
)
from apps.users.serializers import UserShowSerializer


class AlbumSerializers(ModelSerializer):
    class Meta:
        model = AlbumCarModel
        fields = (
            "id",
            "image",
        )


class DetailSerializers(ModelSerializer):
    class Meta:
        model = DetailCarModel
        fields = (
            "id",
            "number",
            "code",
            "fuel",
            "type_fuel",
            "transmission",
            "eugenie",
        )


class CarSerializer(ModelSerializer):
    class Meta:
        model = CarModel
        fields = (
            "id",
            "brand",
            "model",
            "type_car",
            "year",
        )

    def validate(self, attrs):
        if CarModel.objects.filter(
            brand=attrs.get("brand"),
            model=attrs.get("model"),
            type_car=attrs.get("type_car"),
            year=attrs.get("year"),
        ).first():
            raise serializers.ValidationError(
                {"detail": "This object exist, car must be unique"}
            )
        return super().validate(attrs)


class AdvertisementSerializers(ModelSerializer):
    car = CarSerializer(read_only=True)
    owner = UserShowSerializer(read_only=True)
    description = DetailSerializers()
    album = AlbumSerializers(read_only=True, many=True)

    class Meta:
        model = AdvertisementModel
        fields = (
            "id",
            "is_active",
            "is_new",
            "region",
            "price",
            "mileage",
            "info",
            "type_price",
            "album",
            "car",
            "owner",
            "description",
        )

    @atomic
    def create(self, validated_data):
        description = validated_data.pop("description")
        description = DetailCarModel.objects.create(**description)
        car = AdvertisementModel.objects.create(
            **validated_data, description=description
        )
        return car


class UpdateAdvertisementSerializers(ModelSerializer):
    car = CarSerializer(read_only=True)
    owner = UserShowSerializer(read_only=True)
    description = DetailSerializers(read_only=True)
    album = AlbumSerializers(read_only=True, many=True)

    class Meta:
        model = AdvertisementModel
        fields = (
            "id",
            "is_active",
            "is_new",
            "region",
            "price",
            "mileage",
            "info",
            "type_price",
            "album",
            "car",
            "owner",
            "description",
        )


class StaticAdvertisementSerializers(ModelSerializer):
    # user = UserShowSerializer(read_only=True)
    # advertisements = AdvertisementSerializers(read_only=True)

    class Meta:
        model = StaticAdvertisementModel
        fields = (
            "id",
            "view",
            "time",
            # "user",
            # "advertisements",
        )
