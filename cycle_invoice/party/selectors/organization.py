"""Selectors for the Organization model."""
from typing import Any

from django.db.models import QuerySet

from cycle_invoice.common.selectors import get_object
from cycle_invoice.party.filters import OrganizationFilter
from cycle_invoice.party.models import Organization


def organization_list(*, filters: dict[str, Any] | None = None) -> QuerySet[Organization]:
    """Retrieve a list of organizations with optional filters."""
    filters = filters or {}

    qs = Organization.objects.all()

    return OrganizationFilter(filters, queryset=qs).qs


def organization_get(organization_id: str) -> Organization | None:
    """Retrieve a single organization by its ID."""
    return get_object(Organization, search_id=organization_id)
