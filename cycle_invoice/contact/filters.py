"""Filters for contact app models."""
import django_filters

from cycle_invoice.contact.models import Address, Contact, Party, Organisation


class CustomerFilter(django_filters.FilterSet):
    """Filter class for Customer model."""

    class Meta:
        """Metaclass for CustomerFiler."""

        model = Party
        fields = ("uuid", "address", "email", "phone")


class OrganisationFilter(django_filters.FilterSet):
    """Filter class for Organisation model."""

    class Meta:
        """Metaclass for OrganisationFilter."""

        model = Organisation
        fields = ("uuid", "name", "uid")


class ContactFilter(django_filters.FilterSet):
    """Filter class for Contact model."""

    class Meta:
        """Metaclass for ContactFilter."""

        model = Contact
        fields = ("uuid", "first_name", "last_name")


class AddressFilter(django_filters.FilterSet):
    """Filter class for Address model."""

    class Meta:
        """Metaclass for AddressFilter."""

        model = Address
        fields = ("uuid", "street", "number", "city", "zip_code", "country")
