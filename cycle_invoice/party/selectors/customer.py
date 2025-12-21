"""Selectors for the Customer model."""
from typing import Any

from django.db.models import QuerySet

from cycle_invoice.common.selectors import get_object
from cycle_invoice.party.filters import CustomerFilter
from cycle_invoice.party.models import Party


def customer_list(*, filters: dict[str, Any] | None = None) -> QuerySet[Party]:
    """Retrieve a list of customers with optional filters."""
    filters = filters or {}

    qs = Party.objects.all()

    return CustomerFilter(filters, queryset=qs).qs


def customer_get(customer_id: int) -> Party | None:
    """Retrieve a single customer by its ID."""
    return get_object(Party, id=customer_id)
