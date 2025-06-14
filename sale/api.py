"""API views for handling sale operations."""
from rest_framework import serializers
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins import ApiAuthMixin
from api.pagination import LimitOffsetPagination, get_paginated_response
from sale.models import DocumentInvoice
from sale.selectors import invoice_list


class InvoiceListApi(ApiAuthMixin, APIView):
    """API view to handle listing invoices."""

    class Permission(BasePermission):
        """Permission class for invoice listing API."""

        def has_permission(self, request: Request, view: APIView) -> bool:
            """Check if the user has permission to access this view."""
            return request.user.is_authenticated and request.user.has_perm("sale.view_documentinvoice")

    queryset = DocumentInvoice.objects.all()
    permission_classes = (Permission,)

    class FiltersSerializer(serializers.Serializer):
        """Serializer for filtering invoices."""

        id = serializers.IntegerField(required=False, help_text="Filter by invoice ID")
        customer = serializers.IntegerField(required=False, help_text="Filter by customer ID")
        invoice_number = serializers.CharField(required=False, help_text="Filter by invoice number")
        date = serializers.DateField(required=False, help_text="Filter by invoice date")
        due_date = serializers.DateField(required=False, help_text="Filter by invoice due date")

    class OutputSerializer(serializers.ModelSerializer):
        """Serializer for outputting invoice data."""

        class Meta:
            """Metaclass for output serializer."""

            model = DocumentInvoice
            fields = ("id", "customer", "invoice_number", "date", "due_date")

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
