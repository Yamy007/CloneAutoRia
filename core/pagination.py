import math

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        return Response(
            {
                "total_items": count,
                "total_page": math.ceil(count / self.page_size),
                "current_page": self.page.number,
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
