# Generated by Django 4.2.7 on 2023-11-12 01:22

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_alter_typeaccount_expire_premium'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeaccount',
            name='expire_premium',
            field=models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.datetime(2023, 11, 13, 3, 22, 4, 323308)), django.core.validators.MaxValueValidator(datetime.datetime(2024, 2, 10, 3, 22, 4, 323318))]),
        ),
    ]
