"""Test cases for the DocumentItem model."""

from django.test import TestCase

from sale.models import DocumentItem


def fake_document_item() -> DocumentItem:
    """Create a fake document item."""
    return DocumentItem.objects.create(price=5.0, quantity=2, discount=0.1)


class DocumentItemTest(TestCase):
    """Test cases for the DocumentItem model."""

    def test_property_price_str(self) -> None:
        """Test the price_str property."""
        self.assertEqual("5.00", fake_document_item().price_str)

    def test_property_quantity_str(self) -> None:
        """Test the quantity_str property."""
        document_item = fake_document_item()
        self.assertEqual("2", document_item.quantity_str)

        document_item.quantity = 2.22
        self.assertEqual("2.22", document_item.quantity_str)

    def test_property_total(self) -> None:
        """Test the total property."""
        document_item = fake_document_item()
        self.assertEqual(9.00, document_item.total)

        document_item.price = 0.01
        self.assertEqual(0.02, document_item.total)

    def test_property_total_str(self) -> None:
        """Test the total_str property."""
        document_item = fake_document_item()
        self.assertEqual("9.00", document_item.total_str)

    def test_property_discount_str(self) -> None:
        """Test the discount_str property."""
        document_item = fake_document_item()
        self.assertEqual("10.00%", document_item.discount_str)

        document_item.discount = 0
        self.assertEqual("", document_item.discount_str)
