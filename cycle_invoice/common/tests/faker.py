"""Faker instance for tests."""
from faker import Faker

from cycle_invoice.common.tests.faker_providers import SwissProvider, RandomProvider

faker = Faker()

faker.add_provider(SwissProvider)
faker.add_provider(RandomProvider)
