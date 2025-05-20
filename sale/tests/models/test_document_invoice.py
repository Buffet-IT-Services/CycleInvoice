"""Test cases for the DocumentInvoice model."""
import datetime

from django.test import TestCase

from contact.tests.models.test_contact import fake_contact
from sale.models import DocumentInvoice


def fake_document_invoice() -> DocumentInvoice:
    """Create a fake work type."""
    return DocumentInvoice.objects.create(customer=fake_contact(),
                                          invoice_number="INV-12345",
                                          date=datetime.date.today(),
                                          due_date=datetime.date.today() + datetime.timedelta(days=30),
                                          header_text="Header text",
                                          footer_text="Footer text")


class DocumentInvoiceTest(TestCase):
    """Test cases for the DocumentInvoice model."""

    def test_str(self) -> None:
        self.assertEqual("INV-12345 - John Doe", str(fake_document_invoice()))
