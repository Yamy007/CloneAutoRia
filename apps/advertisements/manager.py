from django.db.models import Manager
from rest_framework.generics import get_object_or_404

from core.exceptions.car_exception import PremiumException


class AdvertisementManager(Manager):
    def check_user_is_prem(self, user):
        if user.account.is_premium:
            return True
        if self.filter(owner=user):
            raise PremiumException
