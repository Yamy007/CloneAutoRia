# Generated by Django 4.2.7 on 2023-11-10 12:46

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_profilemodel_name_alter_profilemodel_surname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeaccount',
            name='expire_premium',
            field=models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.datetime(2023, 11, 11, 14, 46, 55, 19884)), django.core.validators.MaxValueValidator(datetime.datetime(2024, 2, 8, 14, 46, 55, 19895))]),
        ),
    ]
