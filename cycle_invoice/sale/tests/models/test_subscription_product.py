"""Test cases for the SubscriptionProduct model."""

from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.sale.models import SubscriptionProduct
from cycle_invoice.sale.tests.models.test_product import fake_product


def fake_subscription_product(save: bool) -> SubscriptionProduct:  # noqa: FBT001
    """Create a fake subscription product."""
    subscription_product = SubscriptionProduct(
        product=fake_product(save=True),
        price=10.00,
        recurrence="monthly"
    )
    if save:
        subscription_product.save(user=get_default_test_user())
    return subscription_product


class SubscriptionProductTest(TestCase):
    """Test cases for the SubscriptionProduct model."""

    def test_str(self) -> None:
        """Test the __str__ of SubscriptionProduct."""
        self.assertEqual("Test Product - Monthly", str(fake_subscription_product(save=False)))
