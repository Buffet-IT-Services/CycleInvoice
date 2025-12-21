"""Factories for party app models."""
import factory
from factory import LazyAttribute

from cycle_invoice.common.tests.factories import BaseFactory
from cycle_invoice.common.tests.faker import faker
from cycle_invoice.party.models import Address, Contact, Organization, OrganizationContact


class AddressFactory(BaseFactory):
    """Factory for the Address model."""

    class Meta:
        """Metaclass for AddressFactory."""

        model = Address

    street = LazyAttribute(lambda _: faker.street_name())
    number = LazyAttribute(lambda _: faker.building_number())
    city = LazyAttribute(lambda _: faker.city())
    zip_code = LazyAttribute(lambda _: faker.postcode())
    country = LazyAttribute(lambda _: faker.country())


class OrganizationFactory(BaseFactory):
    """Factory for the Organization model."""

    class Meta:
        """Metaclass for OrganizationFactory."""

        model = Organization

    name = LazyAttribute(lambda _: faker.company())
    uid = LazyAttribute(lambda _: faker.swiss_uid())
    address = factory.SubFactory(AddressFactory)
    email = LazyAttribute(lambda _: faker.email())
    phone = LazyAttribute(lambda _: faker.phone_number())


class ContactFactory(BaseFactory):
    """Factory for the Contact model."""

    class Meta:
        """Metaclass for ContactFactory."""

        model = Contact

    email = LazyAttribute(lambda _: faker.email())
    first_name = LazyAttribute(lambda _: faker.first_name())
    last_name = LazyAttribute(lambda _: faker.last_name())
    address = factory.SubFactory(AddressFactory)
    phone = LazyAttribute(lambda _: faker.phone_number())


class OrganizationContactFactory(BaseFactory):
    """Factory for the OrganizationContact model."""

    class Meta:
        """Metaclass for OrganizationContactFactory."""

        model = OrganizationContact

    organization = factory.SubFactory(OrganizationFactory)
    contact = factory.SubFactory(ContactFactory)
    role = faker.job()

class Party(BaseFactory):
    """Base factory for Party models."""
