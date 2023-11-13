from django_filters import rest_framework as filter

from apps.users.serializers import UserModelFunction


class UserFilter(filter.FilterSet):
    is_active = filter.BooleanFilter()
    is_block = filter.BooleanFilter()
    is_staff = filter.BooleanFilter()
    is_superuser = filter.BooleanFilter()

    class Meta:
        model = UserModelFunction
        fields = {
            "email": ("istartswith", "iendswith", "icontains"),
            "last_login": ("lt", "lte", "gt", "gte"),
        }

    order = filter.OrderingFilter(
        fields=(
            "id",
            "email",
            "create_at",
            "update_at",
            "last_login",
        )
    )
