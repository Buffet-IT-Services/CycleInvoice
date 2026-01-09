"""Factories for emails app models."""
from factory import SubFactory, LazyAttribute

from cycle_invoice.common.tests.factories import BaseFactory
from cycle_invoice.common.tests.faker import faker
from cycle_invoice.emails.models import Email
from cycle_invoice.party.tests.factories import OrganizationFactory


class EmailFactory(BaseFactory):
    """Factory for the Email model."""

    class Meta:
        """Metaclass for EmailFactory."""

        model = Email

    status = Email.Status.SENDING
    to = SubFactory(OrganizationFactory)
    subject = LazyAttribute(lambda _: faker.sentence())
    html = LazyAttribute(lambda _: faker.paragraph())
    plain_text = LazyAttribute(lambda obj: obj.html)
