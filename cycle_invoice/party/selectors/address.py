"""Selectors for the Address model."""
from typing import Any

from django.db.models import QuerySet

from cycle_invoice.common.selectors import get_object
from cycle_invoice.party.filters import AddressFilter
from cycle_invoice.party.models import Address


def address_list(*, filters: dict[str, Any] | None = None) -> QuerySet[Address]:
    """Retrieve a list of addresses with optional filters."""
    filters = filters or {}

    qs = Address.objects.all()

    return AddressFilter(filters, queryset=qs).qs


def address_get(address_id: str) -> Address | None:
    """Retrieve a single address by its ID."""
    return get_object(Address, search_id=address_id)
