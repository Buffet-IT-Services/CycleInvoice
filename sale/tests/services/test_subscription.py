"""Test cases for the Subscription services."""

import datetime

from django.test import TestCase

from contact.tests.models.test_contact import fake_contact
from sale.tests.models.test_subscription_product import fake_subscription_product


class SubscriptionTest(TestCase):
    """Test cases for the Subscription services."""

    def test_subscription_extension(self) -> None:
        """Test the subscription extension functionality."""
        from sale.models import Subscription
        from sale.services.subscription import SubscriptionExtensionError, subscription_extension

        # Create a subscription
        subscription = Subscription.objects.create(
            product=fake_subscription_product(),
            customer=fake_contact(),
            start_date=datetime.date(2000, 1, 1),
        )

        subscription.cancelled_date = None
        try:
            subscription_extension(subscription.id)
            subscription.refresh_from_db()
            self.assertEqual(datetime.date(2000, 1, 31), subscription.end_billed_date)
        except SubscriptionExtensionError:
            self.fail("SubscriptionExtensionError raised unexpectedly when subscription is not cancelled")

        # Cancel the subscription
        subscription.cancelled_date = datetime.date(2000, 1, 1)
        subscription.save()
        try:
            subscription_extension(subscription.id)
            self.fail("SubscriptionExtensionError doesn't raise when subscription is cancelled")
        except SubscriptionExtensionError:
            self.assertTrue(subscription.is_cancelled)
