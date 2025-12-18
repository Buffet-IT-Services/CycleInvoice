"""Factories for common app models."""

from factory import LazyAttribute
from factory.django import DjangoModelFactory

from cycle_invoice.common.models import User
from cycle_invoice.common.tests import faker


class UserFactory(DjangoModelFactory):
    """Factory for User model."""

    class Meta:
        """Metaclass for UserFactory."""
        model = User

    email = LazyAttribute(lambda _: faker.unique.email())
    first_name = LazyAttribute(lambda _: faker.name())
    last_name = LazyAttribute(lambda _: faker.name())
    is_active = True
    is_staff = True
    is_superuser = True
