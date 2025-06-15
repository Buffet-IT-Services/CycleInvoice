"""Factories for generating test data."""
import factory

from common.models import RandomModel, SimpleModel
from common.tests.base import faker


class RandomModelFactory(factory.django.DjangoModelFactory):
    """Factory for creating RandomModel instances."""

    class Meta:
        """Metaclass for RandomModelFactory."""
        model = RandomModel

    end_date = factory.LazyAttribute(lambda self: faker.date_object())
    start_date = factory.LazyAttribute(lambda self: faker.date_object(end_datetime=self.end_date))


class SimpleModelFactory(factory.django.DjangoModelFactory):
    """Factory for creating SimpleModel instances."""

    class Meta:
        """Metaclass for SimpleModelFactory."""
        model = SimpleModel

    name = factory.LazyAttribute(lambda self: faker.word())
