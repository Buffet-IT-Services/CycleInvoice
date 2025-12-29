"""Tests for the sale model Document."""

from django.test import TestCase

from cycle_invoice.sale.tests.factories import DocumentFactory


class TestDocument(TestCase):
    """Tests for the sale model Document."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.document = DocumentFactory.create()

    def test_document_str(self) -> None:
        """Test Document.__str__()."""
        self.assertEqual(str(self.document), f"{self.document.document_number} - {self.document.party}")
