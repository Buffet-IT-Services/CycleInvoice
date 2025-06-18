"""API views for handling sale operations."""
from django.http import Http404
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cycle_invoice.api.mixins import ApiAuthMixin
from cycle_invoice.api.pagination import LimitOffsetPagination, get_paginated_response
from cycle_invoice.api.serializers import inline_serializer
from cycle_invoice.contact.models import Customer
from cycle_invoice.sale.models import DocumentInvoice
from cycle_invoice.sale.selectors.document_invoice import invoice_get, invoice_list
from cycle_invoice.sale.services.document_invoice import document_invoice_create, document_invoice_update


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
        customer = serializers.IntegerField(source="customer.id")
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

        uuid = serializers.UUIDField()
        invoice_number = serializers.CharField()
        date = serializers.DateField()
        due_date = serializers.DateField()
        header_text = serializers.CharField()
        footer_text = serializers.CharField()
        customer = inline_serializer(fields={
            "uuid": serializers.UUIDField(),
            "name": serializers.CharField(source="__str__"),
        })

    def get(self, request: Request, pk: int, *args, **kwargs) -> Response:  # noqa: ARG002
        """Handle GET requests to retrieve a single invoice."""
        invoice = invoice_get(invoice_id=pk)

        if invoice is None:
            raise Http404

        data = self.OutputSerializer(invoice).data

        return Response(data)


class InvoiceCreateApi(ApiAuthMixin, APIView):
    """API view to handle creating a new invoice."""

    queryset = DocumentInvoice.objects.all()

    class InputSerializer(serializers.Serializer):
        """Serializer for inputting invoice data."""

        invoice_number = serializers.CharField()
        customer = serializers.IntegerField()
        date = serializers.DateField()
        due_date = serializers.DateField()
        header_text = serializers.CharField(required=False, allow_blank=True, allow_null=True)
        footer_text = serializers.CharField(required=False, allow_blank=True, allow_null=True)

        @staticmethod
        def validate_invoice_number(value: str) -> str:
            """Validate that the invoice number is not empty."""
            if DocumentInvoice.objects.filter(invoice_number=value).exists():
                error_message = "There is already an invoice with this number."
                raise serializers.ValidationError(error_message)
            return value

        @staticmethod
        def validate_customer(value: int) -> int:
            """Validate that the customer exists."""
            if not Customer.objects.filter(id=value).exists():
                error_message = "Customer with this ID does not exist."
                raise serializers.ValidationError(error_message)
            return value

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Handle POST requests to create a new invoice."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invoice = document_invoice_create(**serializer.validated_data, user=request.user)

        output_serializer = InvoiceDetailApi.OutputSerializer(invoice)

        return Response(output_serializer.data, status=201)


class InvoiceUpdateApi(ApiAuthMixin, APIView):
    """API view to handle updating an existing invoice."""

    queryset = DocumentInvoice.objects.all()

    class InputSerializer(serializers.Serializer):
        """Serializer for inputting invoice data."""

        invoice_number = serializers.CharField(required=False)
        customer = serializers.IntegerField(required=False)
        date = serializers.DateField(required=False)
        due_date = serializers.DateField(required=False)
        header_text = serializers.CharField(required=False, allow_blank=True)
        footer_text = serializers.CharField(required=False, allow_blank=True)

        @staticmethod
        def validate_invoice_number(value: str) -> str:
            """Validate that the invoice number is not empty."""
            if DocumentInvoice.objects.filter(invoice_number=value).exists():
                error_message = "There is already an invoice with this number."
                raise serializers.ValidationError(error_message)
            return value

        @staticmethod
        def validate_customer(value: int) -> int:
            """Validate that the customer exists."""
            if not Customer.objects.filter(id=value).exists():
                error_message = "Customer with this ID does not exist."
                raise serializers.ValidationError(error_message)
            return value

    def patch(self, request: Request, pk: int, *args, **kwargs) -> Response:
        """Handle PUT requests to update an existing invoice."""
        invoice = invoice_get(invoice_id=pk)

        if invoice is None:
            raise Http404

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invoice = document_invoice_update(invoice=invoice, data=serializer.validated_data, user=request.user)

        data = InvoiceDetailApi.OutputSerializer(invoice).data

        return Response(data, status=201)
