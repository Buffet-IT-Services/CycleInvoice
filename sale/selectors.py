"""Selectors for the sale app."""
from typing import Any

from django.db.models import QuerySet

from sale.filters import DocumentInvoiceFilter
from sale.models import DocumentInvoice


def invoice_list(*, filters: dict[str, Any] | None = None) -> QuerySet[DocumentInvoice]:
    """Retrieve a list of invoices with optional filters."""
    filters = filters or {}

    qs = DocumentInvoice.objects.all()

    return DocumentInvoiceFilter(filters, queryset=qs).qs
