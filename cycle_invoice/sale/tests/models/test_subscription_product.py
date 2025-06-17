"""Test cases for the SubscriptionProduct model."""

from django.test import TestCase

from cycle_invoice.sale.models import Product, SubscriptionProduct
from cycle_invoice.sale.tests.models.test_product import fake_product


def fake_subscription_product() -> SubscriptionProduct:
    """Create a fake subscription product."""
    return SubscriptionProduct.objects.create(product=fake_product(), price=10.00, recurrence="monthly")

class SubscriptionProductTest(TestCase):
    """Test cases for the SubscriptionProduct model."""

    def test_str(self) -> None:
        """Test the __str__ of SubscriptionProduct."""
        product = Product.objects.create(name="Test Product", price=10.00)
        subscription_product = SubscriptionProduct.objects.create(product=product, price=10.00, recurrence="monthly")
        self.assertEqual("Test Product - Monthly", str(subscription_product))
