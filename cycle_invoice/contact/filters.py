"""Filters for contact app models."""
import django_filters

from cycle_invoice.contact.models import Address, Contact, Customer, Organisation


class CustomerFilter(django_filters.FilterSet):
    """Filter class for Customer model."""

    class Meta:
        """Metaclass for CustomerFiler."""

        model = Customer
        fields = ("id", "address")


class OrganisationFilter(django_filters.FilterSet):
    """Filter class for Organisation model."""

    class Meta:
        """Metaclass for OrganisationFilter."""

        model = Organisation
        fields = ("id", "name", "email", "phone", "uid")


class ContactFilter(django_filters.FilterSet):
    """Filter class for Contact model."""

    class Meta:
        """Metaclass for ContactFilter."""

        model = Contact
        fields = ("id", "first_name", "last_name", "email", "phone")


class AddressFilter(django_filters.FilterSet):
    """Filter class for Address model."""

    class Meta:
        """Metaclass for AddressFilter."""

        model = Address
        fields = ("id", "street", "number", "city", "zip_code", "country")
