import requests
from rest_framework.permissions import BasePermission


class IsNotBlock(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and not request.user.is_block
        )


class IsSellerAndNotBlock(IsNotBlock):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            if request.user.account:
                return bool(request.user.account.is_seller)

        return False


class IsSellerOrStaff(IsSellerAndNotBlock):
    def has_permission(self, request, view):
        return bool(super().has_permission(request, view) or request.user.is_staff)


class IsPremiumOrStaff(IsNotBlock):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            if request.user.account:
                if request.user.account.is_seller and request.user.account.is_premium:
                    return True
                if request.user.is_staff:
                    return True

        return False


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff)
