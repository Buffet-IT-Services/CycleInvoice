"""Test cases for the Product model."""

from django.test import TestCase

from cycle_invoice.sale.models import Product


def fake_product() -> Product:
    """Create a fake product."""
    return Product(
        name="Test Product",
        description="This is a test description.",
        price=10.00
    )


class ProductTest(TestCase):
    """Test cases for the Product model."""

    def test_str(self) -> None:
        """Test the __str__ of Product."""
        self.assertEqual("Test Product", str(fake_product()))
