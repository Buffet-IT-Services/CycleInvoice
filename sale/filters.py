"""Filters for sale app models."""
import django_filters

from sale.models import DocumentInvoice


class DocumentInvoiceFilter(django_filters.FilterSet):
    """Filter class for DocumentInvoice model."""

    class Meta:
        """Metaclass for DocumentInvoiceFilter."""
        model = DocumentInvoice
        fields = ("id", "customer", "invoice_number", "date", "due_date")
