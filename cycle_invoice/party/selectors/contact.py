"""Selectors for the Contact model."""
from typing import Any

from django.db.models import QuerySet

from cycle_invoice.common.selectors import get_object
from cycle_invoice.party.filters import ContactFilter
from cycle_invoice.party.models import Contact


def contact_list(*, filters: dict[str, Any] | None = None) -> QuerySet[Contact]:
    """Retrieve a list of contacts with optional filters."""
    filters = filters or {}

    qs = Contact.objects.all()

    return ContactFilter(filters, queryset=qs).qs


def contact_get(contact_id: int) -> Contact | None:
    """Retrieve a single contact by its ID."""
    return get_object(Contact, id=contact_id)
