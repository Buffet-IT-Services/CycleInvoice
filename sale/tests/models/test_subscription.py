"""Test cases for the Subscription model."""
from datetime import datetime

from django.test import TestCase

from sale.models import Subscription


def fake_subscription() -> Subscription:
    """Create a fake subscription."""
    from contact.tests.models.test_contact import fake_contact
    from sale.tests.models.test_subscription_product import fake_subscription_product
    return Subscription.objects.create(
        product=fake_subscription_product(),
        customer=fake_contact(),
        start_date="2000-01-01",
    )


class SubscriptionTest(TestCase):
    """Test cases for the Subscription model."""

    def test__str__(self) -> None:
        """Test the __str__ method."""
        subscription = fake_subscription()
        self.assertEqual("Test Product - John Doe", str(subscription))

    def test_property_is_cancelled(self) -> None:
        """Test the is_cancelled property."""
        subscription = fake_subscription()
        self.assertFalse(subscription.is_cancelled)

        subscription.cancelled_date = datetime.strptime("2023-09-30", "%Y-%m-%d").date()
        subscription.save()
        subscription.refresh_from_db()
        self.assertTrue(subscription.is_cancelled)

    def test_property_next_start_billed_date(self) -> None:
        """Test the next_start_billed_date property."""
        subscription = fake_subscription()
        self.assertEqual(datetime.strptime("2000-01-01", "%Y-%m-%d").date(), subscription.next_start_billed_date)

        subscription.end_billed_date = datetime.strptime("2023-09-30", "%Y-%m-%d").date()
        self.assertEqual(datetime.strptime("2023-10-01", "%Y-%m-%d").date(), subscription.next_start_billed_date)
