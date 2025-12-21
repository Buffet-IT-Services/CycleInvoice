"""Factories for party app models."""

from factory import LazyAttribute

from cycle_invoice.common.tests.factories import BaseFactory
from cycle_invoice.common.tests.faker import faker
from cycle_invoice.party.models import Address


class AddressFactory(BaseFactory):
    """Factory for the Address model."""

    class Meta:
        """Metaclass for AddressFactory."""

        model = Address

    street = LazyAttribute(lambda _: faker.street())
    number = LazyAttribute(lambda _: faker.building_number())
    city = LazyAttribute(lambda _: faker.city())
    zip_code = LazyAttribute(lambda _: faker.postcode())
    country = LazyAttribute(lambda _: faker.country())
