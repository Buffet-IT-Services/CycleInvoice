"""Tests for services related to DocumentInvoice."""
import datetime
from datetime import timedelta

from django.test import TestCase

from contact.tests.models.test_contact import fake_contact
from sale.models import DocumentInvoice
from sale.services.document_invoice import document_invoice_create, document_invoice_update


class DocumentInvoiceServiceTest(TestCase):
    """Test case for document invoice service."""

    def setUp(self) -> None:
        """Set up test data."""
        self.customer = fake_contact()
        self.data = {
            "invoice_number": "INV-2025-001",
            "customer": self.customer.id,
            "date": datetime.datetime.now(tz=datetime.UTC).date(),
            "due_date": datetime.datetime.now(tz=datetime.UTC).date() + timedelta(days=30),
            "header_text": "Header",
            "footer_text": "Footer",
        }

    def test_document_invoice_create(self) -> None:
        """Test creating a document invoice."""
        invoice = document_invoice_create(**self.data)
        self.assertIsInstance(invoice, DocumentInvoice)
        self.assertEqual(invoice.invoice_number, self.data["invoice_number"])
        self.assertEqual(invoice.customer.id, self.customer.id)
        self.assertEqual(invoice.header_text, "Header")
        self.assertEqual(invoice.footer_text, "Footer")

    def test_document_invoice_update(self) -> None:
        """Test updating a document invoice."""
        invoice = document_invoice_create(**self.data)
        update_data = {
            "invoice_number": "INV-2025-002",
            "header_text": "Updated Header",
            "footer_text": "Updated Footer",
            "date": datetime.datetime.now(tz=datetime.UTC).date(),
            "due_date": datetime.datetime.now(tz=datetime.UTC).date() + timedelta(days=60),
            "customer": self.customer.id,
        }
        updated_invoice = document_invoice_update(invoice=invoice, data=update_data)
        self.assertEqual(updated_invoice.invoice_number, "INV-2025-002")
        self.assertEqual(updated_invoice.header_text, "Updated Header")
        self.assertEqual(updated_invoice.footer_text, "Updated Footer")
        self.assertEqual(updated_invoice.due_date,
                         datetime.datetime.now(tz=datetime.UTC).date() + timedelta(days=60))
        self.assertEqual(updated_invoice.customer.id, self.customer.id)
