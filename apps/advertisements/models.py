from datetime import datetime

from django.core import validators
from django.db import models

from apps.advertisements.choices.car_choices import (
    Region,
    TypeCar,
    TypeFuel,
    TypePrice,
    TypeTransmission,
)
from apps.advertisements.manager import AdvertisementManager
from apps.users.models import UserModel
from core.enum.validate import ValidateUser
from core.models import CoreModel


class DetailCarModel(CoreModel):
    class Meta:
        db_table = "description"
        ordering = ["id"]

    number = models.CharField(max_length=35, blank=True)
    code = models.CharField(max_length=45, blank=True)
    fuel = models.FloatField(validators=[validators.MinValueValidator(0)])
    type_fuel = models.CharField(max_length=25, choices=TypeFuel.choices)
    transmission = models.CharField(max_length=25, choices=TypeTransmission.choices)
    eugenie = models.FloatField(
        validators=[validators.MinValueValidator(2), validators.MinValueValidator(100)]
    )


class CarModel(CoreModel):
    class Meta:
        db_table = "cars"
        ordering = ["id"]

    brand = models.CharField(
        max_length=20,
        validators=[validators.RegexValidator(*ValidateUser.NAME_SURNAME.value)],
    )
    model = models.CharField(
        max_length=25, validators=[validators.RegexValidator(*ValidateUser.MODEL.value)]
    )
    type_car = models.CharField(max_length=25, choices=TypeCar.choices)
    year = models.IntegerField(
        validators=[
            validators.MinValueValidator(1900),
            validators.MaxValueValidator(datetime.now().year),
        ]
    )


class AdvertisementModel(CoreModel):
    class Meta:
        db_table = "advertisement"
        ordering = ["id"]

    is_active = models.BooleanField(default=False)
    car = models.ForeignKey(
        CarModel, on_delete=models.CASCADE, related_name="advertisement"
    )
    owner = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="advertisement"
    )
    description = models.ForeignKey(
        DetailCarModel, on_delete=models.CASCADE, related_name="advertisement"
    )

    region = models.CharField(max_length=25, choices=Region.choices)
    price = models.FloatField(validators=[validators.MinValueValidator(100)])
    info = models.TextField()
    type_price = models.CharField(max_length=25, choices=TypePrice.choices)
    mileage = models.FloatField(validators=[validators.MinValueValidator(0)])
    is_new = models.BooleanField()

    objects = AdvertisementManager()


class StaticAdvertisementModel(CoreModel):
    class Meta:
        db_table = "statice_advertisements"
        ordering = ["id"]

    view = models.IntegerField(default=1)
    time = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        UserModel, on_delete=models.SET_NULL, related_name="static", null=True
    )
    advertisements = models.ForeignKey(
        AdvertisementModel, on_delete=models.CASCADE, related_name="static"
    )


class AlbumCarModel(CoreModel):
    class Meta:
        db_table = "album_car"
        ordering = ["id"]

    image = models.ImageField(upload_to="cars/")
    advertisement = models.ForeignKey(
        AdvertisementModel, on_delete=models.CASCADE, related_name="album"
    )


class CounterCheck(models.Model):
    class Meta:
        db_table = "checker"
        ordering = ["id"]

    advertisement = models.ForeignKey(
        AdvertisementModel, on_delete=models.CASCADE, related_name="counter"
    )
    is_send = models.BooleanField(default=False)
    count = models.IntegerField(
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(3)]
    )
