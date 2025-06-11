"""Test cases for the DocumentInvoice model."""

import datetime

from django.test import TestCase

from contact.tests.models.test_contact import fake_contact
from sale.models import DocumentInvoice


def fake_document_invoice() -> DocumentInvoice:
    """Create a fake work type."""
    return DocumentInvoice.objects.create(
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
        invoice = fake_document_invoice()
        from sale.tests.models.test_document_item import fake_document_item
        item = fake_document_item()
        item.invoice = invoice
        item.save()

        from sale.tests.models.test_document_item import fake_document_item_vehicle
        item = fake_document_item_vehicle()
        item.invoice = invoice
        item.save()
        self.assertEqual(29, invoice.total_sum)
