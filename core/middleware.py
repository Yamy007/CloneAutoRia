import os
from datetime import datetime

import pytz
from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.utils import timezone
from rest_framework_simplejwt import authentication


class PremiumStatusMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        response = await self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        timezone = pytz.timezone(os.environ.get("TIMEZONE"))
        current_date = timezone.localize(datetime.now())

        if authentication.JWTAuthentication().authenticate(request):
            request.user = authentication.JWTAuthentication().authenticate(request)[0]
            if request.user.is_authenticated and request.user.account:
                account = request.user.account
                if (
                    account.expire_premium
                    and account.expire_premium.astimezone(timezone) < current_date
                ):
                    account.is_premium = False
                    account.save()
