from django.db import models


class TypeCar(models.TextChoices):
    Hatchback = ("Hatchback",)
    Sedan = ("Sedan",)
    Coupe = ("Coupe",)
    Jeep = "Jeep"


class TypeFuel(models.TextChoices):
    Gas = "Gas"
    Diesel = "Diesel"
    Electricity = "Electricity"
    Hybrid = "Hybrid"
    Gasoline = "Gasoline"


class TypeTransmission(models.TextChoices):
    Manual = "Manual"
    Automatic = "Automatic"


class Region(models.TextChoices):
    Any = "Any"
    Vinnytsia = "Vinnytsia"
    Volyn = "Volyn"
    Dnipropetrovsk = "Dnipropetrovsk"
    Donetsk = "Donetsk"
    Zhytomyr = "Zhytomyr"
    Zakarpattia = "Zakarpattia"
    Zaporizhia = "Zaporizhia"
    Frankivsk = "Frankivsk"
    Kyiv = "Kyiv"
    Kirovohrad = "Kirovohrad"
    Luhansk = "Luhansk"
    Lviv = "Lviv"
    Mykolaiv = "Mykolaiv"
    Odessa = "Odessa"
    Poltava = "Poltava"
    Rivne = "Rivne"
    Sumy = "Sumy"
    Ternopil = "Ternopil"
    Kharkiv = "Kharkiv"
    Kherson = "Kherson"
    Khmelnytskyi = "Khmelnytskyi"
    Cherkasy = "Cherkasy"
    Chernivtsi = "Chernivtsi"
    Chernihiv = "Chernihiv"


class TypePrice(models.TextChoices):
    USD = "USD"
    EUR = "EUR"
    UAH = "UAH"
