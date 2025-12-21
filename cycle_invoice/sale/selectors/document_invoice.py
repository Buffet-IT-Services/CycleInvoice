"""Selectors for the sale app."""
from typing import Any

from django.db.models import QuerySet

from cycle_invoice.common.selectors import get_object
from cycle_invoice.sale.models import Invoice


def invoice_list(*, filters: dict[str, Any] | None = None) -> QuerySet[Invoice]:
    """Retrieve a list of invoices with optional filters."""
    from cycle_invoice.sale.filters import DocumentInvoiceFilter

    filters = filters or {}

    qs = Invoice.objects.all()

    return DocumentInvoiceFilter(filters, queryset=qs).qs


def invoice_get(invoice_id: int | str) -> Invoice | None:
    """Retrieve a single invoice by its ID."""
    return get_object(Invoice, search_id=invoice_id)
