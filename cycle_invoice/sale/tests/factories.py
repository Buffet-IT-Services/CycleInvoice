"""Factories for subscription app models."""

from factory import LazyAttribute, SubFactory

from cycle_invoice.accounting.tests.factories import AccountFactory
from cycle_invoice.common.tests.factories import BaseFactory
from cycle_invoice.common.tests.faker import faker
from cycle_invoice.party.tests.factories import OrganizationFactory
from cycle_invoice.sale.models import Document, DocumentItem, Invoice


class DocumentFactory(BaseFactory):
    """Factory for the Document model."""

    class Meta:
        """Metaclass for DocumentFactory."""

        model = Document

    party = SubFactory(OrganizationFactory)
    document_number = LazyAttribute(lambda _: faker.ean8())
    date = LazyAttribute(lambda _: faker.past_date())
    header_text = LazyAttribute(lambda _: faker.bs())
    footer_text = LazyAttribute(lambda _: faker.bs())


class InvoiceFactory(DocumentFactory):
    """Factory for the Invoice model."""

    class Meta:
        """Metaclass for InvoiceFactory."""

        model = Invoice

    due_date = LazyAttribute(lambda _: faker.future_date())


class DocumentItemFactory(BaseFactory):
    """Factory for the DocumentItem model."""

    class Meta:
        """Metaclass for DocumentItemFactory."""

        model = DocumentItem

    price = LazyAttribute(lambda _: faker.pydecimal(left_digits=2, right_digits=2, positive=True))
    quantity = LazyAttribute(lambda _: faker.pyint(min_value=1, max_value=10))
    party = SubFactory(OrganizationFactory)
    account = SubFactory(AccountFactory)
