"""Filters for sale app models."""
import django_filters

from cycle_invoice.sale.models import DocumentInvoice


class DocumentInvoiceFilter(django_filters.FilterSet):
    """Filter class for DocumentInvoice model."""

    class Meta:
        """Metaclass for DocumentInvoiceFilter."""

        model = DocumentInvoice
        fields = ("uuid", "customer", "invoice_number", "date", "due_date")
