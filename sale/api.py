"""API views for handling sale operations."""
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins import ApiAuthMixin
from api.pagination import LimitOffsetPagination, get_paginated_response
from sale.models import DocumentInvoice
from sale.selectors import invoice_list


class InvoiceListApi(ApiAuthMixin, APIView):
    """API view to handle listing invoices."""

    queryset = DocumentInvoice.objects.all()

    class FiltersSerializer(serializers.Serializer):
        """Serializer for filtering invoices."""

        id = serializers.IntegerField(required=False)
        customer = serializers.IntegerField(required=False)
        invoice_number = serializers.CharField(required=False)
        date = serializers.DateField(required=False)
        due_date = serializers.DateField(required=False)

    class OutputSerializer(serializers.Serializer):
        """Serializer for outputting invoice data."""

        id = serializers.IntegerField()
        customer = serializers.IntegerField(source='customer.id')
        invoice_number = serializers.CharField()
        date = serializers.DateField()
        due_date = serializers.DateField()

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Handle GET requests to list invoices."""
        filters_serializer = self.FiltersSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        invoices = invoice_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=self.OutputSerializer,
            queryset=invoices,
            request=request,
            view=self,
        )
