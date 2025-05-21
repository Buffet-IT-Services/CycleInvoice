"""Test cases for the Product model."""

from django.test import TestCase

from sale.models import Product

def fake_product() -> Product:
    """Create a fake product."""
    return Product.objects.create(name="Test Product", description="This is a test description.", price=10.00)

class ProductTest(TestCase):
    """Test cases for the Product model."""

    def test_str(self) -> None:
        """Test the __str__ of Product."""
        product = Product.objects.create(name="Test Product", price=10.00)
        self.assertEqual("Test Product", str(product))
