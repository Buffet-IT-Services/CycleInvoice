"""Test cases for the Subscription model."""

from django.test import TestCase
from recurring.models import CalendarEntry

from contact.models import Organisation
from sale.models import Product, SubscriptionProduct, Subscription


class SubscriptionTest(TestCase):
    """Test cases for the Subscription model."""

    def test_str(self) -> None:
        """Test the __str__ of Subscription."""
        product = Product.objects.create(name="Test Product", price=10.00)
        subscription_product = SubscriptionProduct.objects.create(product=product, price=10.00, recurrence="monthly")
        organisation = Organisation.objects.create(name="Test Organisation")
        calendar_entry = CalendarEntry.objects.create(name="Test Calendar Entry")

        subscription = Subscription.objects.create(product=subscription_product, customer=organisation,
                                                   calendar_entry=calendar_entry)
        self.assertEqual("Test Product - Test Organisation", str(subscription))
