"""Tests for the model product of the app product."""
from django.test import TestCase

from cycle_invoice.product.tests.factories import ProductFactory


class TestProduct(TestCase):
    """Tests for the model product of the app product."""

    def test_str(self) -> None:
        """Test Product.__str__()."""
        product = ProductFactory()
        self.assertEqual(str(product), product.name)
