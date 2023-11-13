from django.core import validators
from django.db import models


class CoreModel(models.Model):
    class Meta:
        abstract = True

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class DetailPremiumModel(models.Model):
    class Meta:
        db_table = "premium_detail"

    days = models.IntegerField(validators.MinValueValidator(1))
    price = models.FloatField(
        validators.MinValueValidator(1), blank=True, null=True
    )  # not use now
    # another fields...
