"""Tests for the sale model DocumentItem."""
from decimal import Decimal

from django.test import TestCase

from cycle_invoice.common.models import DiscountType
from cycle_invoice.sale.tests.factories import DocumentItemFactory


class TestDocumentItem(TestCase):
    """Tests for the sale model DocumentItem."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.document_item = DocumentItemFactory.build()

    def test_documentitem_price_str(self) -> None:
        """Test the string representation of DocumentItem price."""
        self.document_item.price = 1.2345
        self.assertEqual(self.document_item.price_str, f"{self.document_item.price:.2f}")

    def test_documentitem_quantity_str(self) -> None:
        """Test the string representation of DocumentItem quantity."""
        self.document_item.quantity = 1.2345
        self.assertEqual(self.document_item.quantity_str, f"{self.document_item.quantity:.2f}")

    def test_documentitem_quantity_str_integer(self) -> None:
        """Test the string representation of DocumentItem quantity."""
        self.document_item.quantity = 1
        self.assertEqual(self.document_item.quantity_str, "1")

    def test_documentitem_total(self) -> None:
        """Test DocumentItem.total."""
        self.assertEqual(self.document_item.total, self.document_item.price * self.document_item.quantity)

    def test_documentitem_total_discount_percent(self) -> None:
        """Test DocumentItem.total with discount."""
        self.document_item.discount_value = 10
        self.document_item.discount_type = DiscountType.PERCENT
        self.assertEqual(self.document_item.total,
                         round(self.document_item.price * self.document_item.quantity
                               * Decimal((1 - (self.document_item.discount_value / 100))), 2))

    def test_documentitem_total_discount_fixed(self) -> None:
        """Test DocumentItem.total with discount."""
        self.document_item.discount_value = 1
        self.document_item.discount_type = DiscountType.ABSOLUTE
        self.assertEqual(self.document_item.total, self.document_item.price * self.document_item.quantity - 1)

    def test_documentitem_total_str(self) -> None:
        """Test DocumentItem.total_str."""
        self.document_item.quantity = 1.2345
        self.document_item.price = 1.2345
        self.assertEqual(self.document_item.total_str, f"{self.document_item.total:.2f}")

    def test_documentitem_discount_str_none(self) -> None:
        """Test DocumentItem.discount_str."""
        self.assertEqual(self.document_item.discount_str, "")

    def test_documentitem_discount_str_percent(self) -> None:
        """Test DocumentItem.discount_str."""
        self.document_item.discount_value = 10
        self.document_item.discount_type = DiscountType.PERCENT
        self.assertEqual(self.document_item.discount_str, f"{(100 * self.document_item.discount_value):.2f}%")

    def test_documentitem_discount_str_fixed(self) -> None:
        """Test DocumentItem.discount_str."""
        self.document_item.discount_value = 1
        self.document_item.discount_type = DiscountType.ABSOLUTE
        self.assertEqual(self.document_item.discount_str, f"-{self.document_item.discount_value:.2f}")
