"""Filters for sale app models."""
import django_filters

from cycle_invoice.sale.models import Invoice


class DocumentInvoiceFilter(django_filters.FilterSet):
    """Filter class for DocumentInvoice model."""

    class Meta:
        """Metaclass for DocumentInvoiceFilter."""

        model = Invoice
        fields = ("uuid", "party", "date", "due_date")
