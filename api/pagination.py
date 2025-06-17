"""Pagination for API responses."""
from collections import OrderedDict

from django.db.models import QuerySet
from rest_framework.pagination import BasePagination
from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView


def get_paginated_response(
        *,
        pagination_class: type[BasePagination],
        serializer_class: type[Serializer],
        queryset: QuerySet,
        request: Request,
        view: APIView
) -> Response:
    """Get a paginated response for the given queryset."""
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return Response(data=serializer.data)


class LimitOffsetPagination(_LimitOffsetPagination):
    """Pagination class that supports limit and offset for API responses."""

    default_limit = 10
    max_limit = 100

    def get_paginated_data(self, data: list) -> OrderedDict:
        """Return the paginated data in a specific format."""
        return OrderedDict(
            [
                ("limit", self.limit),
                ("offset", self.offset),
                ("count", self.count),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("results", data),
            ]
        )

    def get_paginated_response(self, data: list) -> Response:
        """
        We redefine this method in order to return `limit` and `offset`.

        This is used by the frontend to construct the pagination itself.
        """
        return Response(self.get_paginated_data(data=data))
