"""Selectors for the Organisation model."""
from typing import Any

from django.db.models import QuerySet

from cycle_invoice.common.selectors import get_object
from cycle_invoice.party.filters import OrganisationFilter
from cycle_invoice.party.models import Organisation


def organisation_list(*, filters: dict[str, Any] | None = None) -> QuerySet[Organisation]:
    """Retrieve a list of organisations with optional filters."""
    filters = filters or {}

    qs = Organisation.objects.all()

    return OrganisationFilter(filters, queryset=qs).qs


def organisation_get(organisation_id: int) -> Organisation | None:
    """Retrieve a single organisation by its ID."""
    return get_object(Organisation, id=organisation_id)
