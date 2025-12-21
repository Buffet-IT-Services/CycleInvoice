"""Filters for contact app models."""
import django_filters

from cycle_invoice.party.models import Address, Contact, Organization, Party


class PartyFilter(django_filters.FilterSet):
    """Filter class for the Customer model."""

    class Meta:
        """Metaclass for CustomerFiler."""

        model = Party
        fields = ("uuid", "address", "email", "phone")


class OrganizationFilter(django_filters.FilterSet):
    """Filter class for the Organization model."""

    class Meta:
        """Metaclass for OrganizationFilter."""

        model = Organization
        fields = ("uuid", "name", "uid")


class ContactFilter(django_filters.FilterSet):
    """Filter class for the Contact model."""

    class Meta:
        """Metaclass for ContactFilter."""

        model = Contact
        fields = ("uuid", "first_name", "last_name")


class AddressFilter(django_filters.FilterSet):
    """Filter class for the Address model."""

    class Meta:
        """Metaclass for AddressFilter."""

        model = Address
        fields = ("uuid", "street", "number", "city", "zip_code", "country")
