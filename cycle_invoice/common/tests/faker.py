"""Faker instance for tests."""
from faker import Faker

from cycle_invoice.common.tests.faker_providers import SwissUIDProvider

faker = Faker()

faker.add_provider(SwissUIDProvider)
