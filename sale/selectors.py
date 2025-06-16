"""Selectors for the sale app."""
from typing import Any

from django.db.models import QuerySet

from common.selectors import get_object
from sale.filters import DocumentInvoiceFilter
from sale.models import DocumentInvoice


def invoice_list(*, filters: dict[str, Any] | None = None) -> QuerySet[DocumentInvoice]:
    """Retrieve a list of invoices with optional filters."""
    filters = filters or {}

    qs = DocumentInvoice.objects.all()

    return DocumentInvoiceFilter(filters, queryset=qs).qs

def invoice_get(invoice_id: int) -> DocumentInvoice | None:
    """Retrieve a single invoice by its ID."""
    return get_object(DocumentInvoice, id=invoice_id)
