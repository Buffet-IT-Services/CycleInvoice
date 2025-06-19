"""Test cases for selectors in the sale application."""
from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_user
from cycle_invoice.sale.selectors.document_invoice import invoice_get, invoice_list
from cycle_invoice.sale.tests.models.test_document_invoice import fake_document_invoice_with_invoice_number


class SelectorsDocumentInvoiceTest(TestCase):
    """Test cases for selectors related to DocumentInvoice."""

    def setUp(self) -> None:
        """Set up test data for DocumentInvoice selectors."""
        user = get_default_user()
        self.invoice1 = fake_document_invoice_with_invoice_number(
            invoice_number="INV-1",
            save=True,
        )
        self.invoice2 = fake_document_invoice_with_invoice_number(
            invoice_number="INV-2",
            save=True,
        )

    def test_invoice_list_returns_all(self) -> None:
        """Test that invoice_list returns all invoices."""
        qs = invoice_list()
        self.assertIn(self.invoice1, qs)
        self.assertIn(self.invoice2, qs)
        self.assertEqual(qs.count(), 2)

    def test_invoice_get_returns_invoice(self) -> None:
        """Test that invoice_get returns the correct invoice."""
        invoice = invoice_get(self.invoice1.id)
        self.assertEqual(invoice, self.invoice1)

    def test_invoice_get_returns_none_for_invalid_id(self) -> None:
        """Test that invoice_get returns None for an invalid ID."""
        invoice = invoice_get(99999)
        self.assertIsNone(invoice)
