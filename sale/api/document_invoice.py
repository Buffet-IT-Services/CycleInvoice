"""API views for handling sale operations."""
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins import ApiAuthMixin
from api.pagination import LimitOffsetPagination, get_paginated_response
from api.serializers import inline_serializer
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

class InvoiceDetailApi(ApiAuthMixin, APIView):
    """API view to handle retrieving a single invoice."""

    queryset = DocumentInvoice.objects.all()

    class OutputSerializer(serializers.Serializer):
        """Serializer for outputting invoice data."""

        id = serializers.IntegerField()
        invoice_number = serializers.CharField()
        date = serializers.DateField()
        due_date = serializers.DateField()
        header_text = serializers.CharField()
        footer_text = serializers.CharField()
        customer = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'name': serializers.CharField(source="__str__"),
        })

    def get(self, request: Request, pk: int, *args, **kwargs) -> Response:
        """Handle GET requests to retrieve a single invoice."""
        try:
            invoice = self.queryset.get(pk=pk)
        except DocumentInvoice.DoesNotExist:
            return Response({'detail': 'Invoice not found'}, status=404)

        serializer = self.OutputSerializer(invoice)
        return Response(serializer.data)