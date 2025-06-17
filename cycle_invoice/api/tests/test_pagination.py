"""Tests for API pagination."""
from collections import OrderedDict
from unittest.mock import MagicMock

from django.db.models import QuerySet
from django.test import TestCase
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from cycle_invoice.api.pagination import LimitOffsetPagination, get_paginated_response
from cycle_invoice.common.models import SimpleModel


class PaginationTest(TestCase):
    """Tests for API pagination."""

    def setUp(self) -> None:
        """Set up the test environment."""
        SimpleModel.objects.all().delete()
        for i in range(1, 6):
            SimpleModel.objects.create(name=f"Name {i}")

    def test_get_paginated_response_with_real_pagination(self) -> None:
        """Test the get_paginated_response function with real pagination."""

        class DummySerializer(Serializer):
            def to_representation(self, obj: object) -> str:
                return obj.name

        class SmallPagePagination(PageNumberPagination):
            page_size = 2

        queryset = SimpleModel.objects.order_by("id")
        request = MagicMock()
        request.query_params = {"page": 1}
        view = APIView()
        response = get_paginated_response(
            pagination_class=SmallPagePagination,
            serializer_class=DummySerializer,
            queryset=queryset,
            request=request,
            view=view
        )
        self.assertIsInstance(response, Response)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["results"], ["Name 1", "Name 2"])
        self.assertEqual(response.data["count"], 5)

    def test_get_paginated_response_without_pagination_real(self) -> None:
        """Test the get_paginated_response function without pagination."""

        class DummySerializer(Serializer):
            def to_representation(self, obj: object) -> str:
                return obj.name

        class NoPagination(PageNumberPagination):
            def paginate_queryset(self, inner_queryset: QuerySet, inner_request: Request,  # noqa: ARG002
                                  inner_view: APIView = None) -> None:  # noqa: ARG002
                return None  # disables pagination

        queryset = SimpleModel.objects.order_by("id")
        request = MagicMock()
        request.query_params = {}
        view = APIView()
        response = get_paginated_response(
            pagination_class=NoPagination,
            serializer_class=DummySerializer,
            queryset=queryset,
            request=request,
            view=view
        )
        self.assertIsInstance(response, Response)
        self.assertEqual(response.data, ["Name 1", "Name 2", "Name 3", "Name 4", "Name 5"])


class LimitOffsetPaginationTest(TestCase):
    """Tests for LimitOffsetPagination."""

    def test_default_limit_and_max_limit(self) -> None:
        """Test the default limit and max limit of LimitOffsetPagination."""
        paginator = LimitOffsetPagination()
        self.assertEqual(paginator.default_limit, 10)
        self.assertEqual(paginator.max_limit, 100)

    def test_get_paginated_data_format(self) -> None:
        """Test the format of the data returned by get_paginated_data."""
        paginator = LimitOffsetPagination()
        paginator.limit = 10
        paginator.offset = 0
        paginator.count = 42
        paginator.get_next_link = lambda: "next-url"
        paginator.get_previous_link = lambda: None
        data = [1, 2, 3]
        paginated = paginator.get_paginated_data(data)
        self.assertIsInstance(paginated, OrderedDict)
        self.assertEqual(paginated["limit"], 10)
        self.assertEqual(paginated["offset"], 0)
        self.assertEqual(paginated["count"], 42)
        self.assertEqual(paginated["next"], "next-url")
        self.assertIsNone(paginated["previous"])
        self.assertEqual(paginated["results"], data)

    def test_get_paginated_response(self) -> None:
        """Test the get_paginated_response method of LimitOffsetPagination."""
        paginator = LimitOffsetPagination()
        paginator.limit = 5
        paginator.offset = 2
        paginator.count = 20
        paginator.get_next_link = lambda: "next-url"
        paginator.get_previous_link = lambda: "prev-url"
        data = [1, 2, 3]
        response = paginator.get_paginated_response(data)
        self.assertEqual(response.data["limit"], 5)
        self.assertEqual(response.data["offset"], 2)
        self.assertEqual(response.data["count"], 20)
        self.assertEqual(response.data["next"], "next-url")
        self.assertEqual(response.data["previous"], "prev-url")
        self.assertEqual(response.data["results"], data)
