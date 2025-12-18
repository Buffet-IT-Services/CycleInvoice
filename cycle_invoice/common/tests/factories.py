"""Factories for common app models."""
from typing import Any

from factory import LazyAttribute
from factory.django import DjangoModelFactory

from cycle_invoice.common.models import User, BaseModel
from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.common.tests.faker import faker


class BaseFactory(DjangoModelFactory):
    """
    Base factory for all models inheriting from BaseModel.

    Ensures that `save(user=...)` is always called, so audit fields
    (created_by, updated_by, history user) are set consistently.
    """

    class Meta:
        """Metaclass for BaseFactory."""

        abstract = True

    @classmethod
    def _create(cls, model_class: type[BaseModel], *args: Any, **kwargs: Any) -> BaseModel:
        """
        Create a model instance using the system user unless explicitly overridden.
        """

        user = kwargs.pop("user", None) or get_system_user()

        obj = model_class(*args, **kwargs)
        obj.save(user=user)
        return obj


class UserFactory(BaseFactory):
    """Factory for the User model."""

    class Meta:
        """Metaclass for UserFactory."""
        model = User

    email = LazyAttribute(lambda _: faker.unique.email())
    first_name = LazyAttribute(lambda _: faker.name())
    last_name = LazyAttribute(lambda _: faker.name())
    is_active = True
    is_staff = True
    is_superuser = True
