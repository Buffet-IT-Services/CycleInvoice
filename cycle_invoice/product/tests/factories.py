"""Factories for product app product."""
import secrets

from factory import LazyAttribute, SubFactory

from cycle_invoice.accounting.tests.factories import AccountFactory
from cycle_invoice.common.tests.factories import BaseFactory
from cycle_invoice.common.tests.faker import faker
from cycle_invoice.product.models import Product


class ProductFactory(BaseFactory):
    """Factory for the Product model."""

    class Meta:
        """Metaclass for AddressFactory."""

        model = Product

    name = LazyAttribute(lambda _: faker.bs())
    description = LazyAttribute(lambda _: faker.bs())
    account_buy = SubFactory(AccountFactory)
    account_sell = SubFactory(AccountFactory)
    price = LazyAttribute(lambda _: secrets.randbelow(10000))
