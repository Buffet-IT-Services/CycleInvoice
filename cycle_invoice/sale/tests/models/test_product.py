"""Test cases for the Product model."""

from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.sale.models import Product


def fake_product(save: bool) -> Product:
    """Create a fake product."""
    product = Product(
        name="Test Product",
        description="This is a test description.",
        price=10.00
    )
    if save:
        product.save(user=get_default_test_user())
    return product


class ProductTest(TestCase):
    """Test cases for the Product model."""

    def test_str(self) -> None:
        """Test the __str__ of Product."""
        self.assertEqual("Test Product", str(fake_product(save=False)))
