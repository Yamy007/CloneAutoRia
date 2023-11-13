# Generated by Django 4.2.7 on 2023-11-12 23:49

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AdvertisementModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_new", models.BooleanField()),
                ("is_active", models.BooleanField(default=False)),
                (
                    "region",
                    models.CharField(
                        choices=[
                            ("Any", "Any"),
                            ("Vinnytsia", "Vinnytsia"),
                            ("Volyn", "Volyn"),
                            ("Dnipropetrovsk", "Dnipropetrovsk"),
                            ("Donetsk", "Donetsk"),
                            ("Zhytomyr", "Zhytomyr"),
                            ("Zakarpattia", "Zakarpattia"),
                            ("Zaporizhia", "Zaporizhia"),
                            ("Frankivsk", "Frankivsk"),
                            ("Kyiv", "Kyiv"),
                            ("Kirovohrad", "Kirovohrad"),
                            ("Luhansk", "Luhansk"),
                            ("Lviv", "Lviv"),
                            ("Mykolaiv", "Mykolaiv"),
                            ("Odessa", "Odessa"),
                            ("Poltava", "Poltava"),
                            ("Rivne", "Rivne"),
                            ("Sumy", "Sumy"),
                            ("Ternopil", "Ternopil"),
                            ("Kharkiv", "Kharkiv"),
                            ("Kherson", "Kherson"),
                            ("Khmelnytskyi", "Khmelnytskyi"),
                            ("Cherkasy", "Cherkasy"),
                            ("Chernivtsi", "Chernivtsi"),
                            ("Chernihiv", "Chernihiv"),
                        ],
                        max_length=25,
                    ),
                ),
                (
                    "price",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(100)]
                    ),
                ),
                (
                    "type_price",
                    models.CharField(
                        choices=[("USD", "Usd"), ("EUR", "Eur"), ("UAH", "Uah")],
                        max_length=25,
                    ),
                ),
                ("info", models.TextField()),
                (
                    "mileage",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("update_at", models.DateTimeField(auto_now=True)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "advertisement",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="CarModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "brand",
                    models.CharField(
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                "[A-Z][a-z]{2,24}",
                                "Fields must have only letters and start with upper",
                            )
                        ],
                    ),
                ),
                (
                    "model",
                    models.CharField(
                        max_length=25,
                        validators=[
                            django.core.validators.RegexValidator(
                                "[A-Z][a-z0-9]{2,24}",
                                "Fields must have  letters or number and start with upper",
                            )
                        ],
                    ),
                ),
                (
                    "type_car",
                    models.CharField(
                        choices=[
                            ("Hatchback", "Hatchback"),
                            ("Sedan", "Sedan"),
                            ("Coupe", "Coupe"),
                            ("Jeep", "Jeep"),
                        ],
                        max_length=25,
                    ),
                ),
                (
                    "year",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1900),
                            django.core.validators.MaxValueValidator(2023),
                        ]
                    ),
                ),
                ("update_at", models.DateTimeField(auto_now=True)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "cars",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="DetailCarModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.CharField(blank=True, max_length=35)),
                ("code", models.CharField(blank=True, max_length=45)),
                (
                    "fuel",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "type_fuel",
                    models.CharField(
                        choices=[
                            ("Gas", "Gas"),
                            ("Diesel", "Diesel"),
                            ("Electricity", "Electricity"),
                            ("Hybrid", "Hybrid"),
                            ("Gasoline", "Gasoline"),
                        ],
                        max_length=25,
                    ),
                ),
                (
                    "transmission",
                    models.CharField(
                        choices=[("Manual", "Manual"), ("Automatic", "Automatic")],
                        max_length=25,
                    ),
                ),
                (
                    "eugenie",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(2),
                            django.core.validators.MinValueValidator(100),
                        ]
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "description",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="StaticAdvertisementModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("view", models.IntegerField(default=1)),
                ("time", models.DateField(auto_now_add=True)),
                (
                    "advertisements",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="static",
                        to="advertisements.advertisementmodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="static",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("update_at", models.DateTimeField(auto_now=True)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "statice_advertisements",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="CounterCheck",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_send", models.BooleanField(default=False)),
                (
                    "count",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(3),
                        ]
                    ),
                ),
                (
                    "advertisement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="counter",
                        to="advertisements.advertisementmodel",
                    ),
                ),
            ],
            options={
                "db_table": "checker",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="AlbumCarModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="cars/")),
                (
                    "advertisement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="album",
                        to="advertisements.advertisementmodel",
                    ),
                ),
                ("update_at", models.DateTimeField(auto_now=True)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "album_car",
                "ordering": ["id"],
            },
        ),
        migrations.AddField(
            model_name="advertisementmodel",
            name="car",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="advertisement",
                to="advertisements.carmodel",
            ),
        ),
        migrations.AddField(
            model_name="advertisementmodel",
            name="description",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="advertisement",
                to="advertisements.detailcarmodel",
            ),
        ),
        migrations.AddField(
            model_name="advertisementmodel",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="advertisement",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
