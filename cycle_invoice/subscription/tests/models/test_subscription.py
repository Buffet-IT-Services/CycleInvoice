"""Test cases for the Subscription model."""
import datetime

from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.contact.tests.models.test_contact import fake_contact
from cycle_invoice.sale.models import Subscription
from cycle_invoice.subscription.tests.models.test_subscription_product import fake_subscription_product


def fake_subscription(save: bool) -> Subscription:  # noqa: FBT001
    """Create a fake subscription."""
    subscription = Subscription(
        product=fake_subscription_product(save=True),
        customer=fake_contact(save=True),
        start_date=datetime.date(2000, 1, 1),
    )
    if save:
        subscription.save(user=get_default_test_user())
    return subscription


class SubscriptionTest(TestCase):
    """Test cases for the Subscription model."""

    def test__str__(self) -> None:
        """Test the __str__ method."""
        self.assertEqual("Test Product - John Doe", str(fake_subscription(save=False)))

    def test_property_is_cancelled(self) -> None:
        """Test the is_cancelled property."""
        subscription = fake_subscription(save=True)
        self.assertFalse(subscription.is_cancelled)

        subscription.cancelled_date = datetime.date(2001, 12, 31)
        user = get_default_test_user()
        subscription.save(user=user)
        subscription.refresh_from_db()
        self.assertTrue(subscription.is_cancelled)

    def test_property_next_start_billed_date(self) -> None:
        """Test the next_start_billed_date property."""
        subscription = fake_subscription(save=False)
        self.assertEqual(datetime.date(2000, 1, 1), subscription.next_start_billed_date)

        subscription.end_billed_date = datetime.date(2023, 9, 30)
        self.assertEqual(datetime.date(2023, 10, 1), subscription.next_start_billed_date)

    def test_property_next_end_billed_date(self) -> None:
        """Test the next_end_billed_date property."""
        subscription = fake_subscription(save=False)
        self.assertEqual(datetime.date(2000, 1, 31), subscription.next_end_billed_date)

        subscription.end_billed_date = datetime.date(2023, 9, 30)
        self.assertEqual(datetime.date(2023, 10, 31), subscription.next_end_billed_date)

        subscription.product.recurrence = "yearly"
        self.assertEqual(datetime.date(2024, 9, 30), subscription.next_end_billed_date)

        subscription.product.recurrence = "unknown"
        self.assertRaises(ValueError, lambda: subscription.next_end_billed_date)
