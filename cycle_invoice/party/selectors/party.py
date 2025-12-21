"""Selectors for the Customer model."""
from typing import Any

from django.db.models import QuerySet

from cycle_invoice.common.selectors import get_object
from cycle_invoice.party.filters import PartyFilter
from cycle_invoice.party.models import Party


def party_list(*, filters: dict[str, Any] | None = None) -> QuerySet[Party]:
    """Retrieve a list of customers with optional filters."""
    filters = filters or {}

    qs = Party.objects.all()

    return PartyFilter(filters, queryset=qs).qs


def party_get(customer_id: str) -> Party | None:
    """Retrieve a single customer by its ID."""
    return get_object(Party, search_id=customer_id)
