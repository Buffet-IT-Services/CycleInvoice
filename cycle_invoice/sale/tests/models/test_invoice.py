"""Tests for the sale model Invoice."""
from decimal import Decimal

from django.test import TestCase

from cycle_invoice.common.models import DiscountType
from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.sale.tests.factories import DocumentItemFactory, InvoiceFactory


class TestInvoice(TestCase):
    """Tests for the sale model Invoice."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.invoice = InvoiceFactory.create()
        self.item_1 = DocumentItemFactory.create(document=self.invoice, party=self.invoice.party)
        self.item_2 = DocumentItemFactory.create(party=self.invoice.party)
        self.system_user = get_system_user()

    def test_invoice_total_sum(self) -> None:
        """Test Invoice.total_sum."""
        self.item_2.document = self.invoice
        self.item_2.save(user=self.system_user)
        self.assertEqual(self.invoice.total_sum,
                         self.item_1.quantity * self.item_1.price + self.item_2.quantity * self.item_2.price)

    def test_invoice_total_sum_discount_percent(self) -> None:
        """Test Invoice.total_sum with discount."""
        item = self.item_1
        item.discount_value = 10
        item.discount_type = DiscountType.PERCENT
        item.save(user=self.system_user)
        multiplier = Decimal(1) - (Decimal(item.discount_value) / Decimal(100))
        expected = round(item.price * item.quantity * multiplier, 2)
        self.assertEqual(self.invoice.total_sum, expected)
