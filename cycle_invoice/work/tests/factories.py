"""Factories for work app models."""
import secrets

from factory import LazyAttribute, SubFactory

from cycle_invoice.accounting.tests.factories import AccountFactory
from cycle_invoice.common.tests.factories import BaseFactory
from cycle_invoice.common.tests.faker import faker
from cycle_invoice.work.models import WorkType


class WorkTypeFactory(BaseFactory):
    """Factory for the WorkType model."""

    class Meta:
        """Metaclass for WorkTypeFactory."""

        model = WorkType

    name = LazyAttribute(lambda _: f"{faker.bs()} Work Type")
    account = SubFactory(AccountFactory)
    price_per_hour = LazyAttribute(lambda _: secrets.randbelow(100) * 10)
