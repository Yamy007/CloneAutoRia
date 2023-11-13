from django_filters import rest_framework as filter

from .models import StaticAdvertisementModel


class StaticFilter(filter.FilterSet):
    time = filter.DateFromToRangeFilter()

    class Meta:
        model = StaticAdvertisementModel
        fields = ["time"]

    order = filter.OrderingFilter(
        fields=(
            "id",
            "time",
        )
    )
