"""Factories for accounting app models."""
import secrets
import string

from factory import LazyAttribute

from cycle_invoice.accounting.models import Account
from cycle_invoice.common.tests.factories import BaseFactory
from cycle_invoice.common.tests.faker import faker


class AccountFactory(BaseFactory):
    """Factory for the Account model."""

    class Meta:
        """Metaclass for AddressFactory."""

        model = Account

    name = LazyAttribute(lambda _: f"{faker.bs()} Expense")
    number = LazyAttribute(lambda _: "".join(
        secrets.choice(string.ascii_uppercase + string.digits)
        for _ in range(secrets.randbelow(15) + 6)
    ))
