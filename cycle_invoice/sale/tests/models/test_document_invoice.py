"""Test cases for the DocumentInvoice model."""

import datetime

from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_user
from cycle_invoice.contact.tests.models.test_contact import fake_contact
from cycle_invoice.sale.models import DocumentInvoice
from cycle_invoice.sale.tests.models.test_document_item import (
    fake_document_item_product,
    fake_document_item_subscription,
)


def fake_document_invoice_with_invoice_number(invoice_number: str) -> DocumentInvoice:
    """Create a fake invoice with provided invoice number."""
    return DocumentInvoice(
        customer=fake_contact(),
        invoice_number=invoice_number,
        date=datetime.datetime.now(tz=datetime.UTC).date(),
        due_date=datetime.datetime.now(tz=datetime.UTC).date() + datetime.timedelta(days=30),
        header_text="Header text",
        footer_text="Footer text",
    )


def fake_document_invoice() -> DocumentInvoice:
    """Create a fake invoice with a default invoice number."""
    return DocumentInvoice(
        customer=fake_contact(),
        invoice_number="INV-12345",
        date=datetime.datetime.now(tz=datetime.UTC).date(),
        due_date=datetime.datetime.now(tz=datetime.UTC).date() + datetime.timedelta(days=30),
        header_text="Header text",
        footer_text="Footer text",
    )


class DocumentInvoiceTest(TestCase):
    """Test cases for the DocumentInvoice model."""

    def test_str(self) -> None:
        """Test the string representation of the DocumentInvoice model."""
        self.assertEqual("INV-12345 - John Doe", str(fake_document_invoice()))

    def test_total_sum(self) -> None:
        """Test the total sum of the DocumentInvoice model."""
        user = get_default_user()
        invoice = fake_document_invoice()
        item = fake_document_item_subscription()
        item.invoice = invoice
        item.customer.save(user=user)
        item.invoice.customer.save(user=user)
        item.invoice.save(user=user)
        item.product.save(user=user)
        item.subscription.product.save(user=user)
        item.subscription.customer.save(user=user)
        item.subscription.save(user=user)
        item.save(user=user)

        item = fake_document_item_product()
        item.invoice = invoice
        item.customer.save(user=user)
        item.product.save(user=user)
        item.save(user=user)
        self.assertEqual(19, invoice.total_sum)
