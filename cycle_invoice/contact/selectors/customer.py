"""Selectors for the Customer model."""
from typing import Any

from django.db.models import QuerySet

from cycle_invoice.common.selectors import get_object
from cycle_invoice.contact.filters import CustomerFilter
from cycle_invoice.contact.models import Customer


def customer_list(*, filters: dict[str, Any] | None = None) -> QuerySet[Customer]:
    """Retrieve a list of customers with optional filters."""
    filters = filters or {}

    qs = Customer.objects.all()

    return CustomerFilter(filters, queryset=qs).qs


def customer_get(customer_id: int) -> Customer | None:
    """Retrieve a single customer by its ID."""
    return get_object(Customer, id=customer_id)
