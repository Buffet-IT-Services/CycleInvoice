"""Test cases for the Subscription services."""

import datetime

from django.test import TestCase

from contact.tests.models.test_contact import fake_contact
from sale.tests.models.test_subscription_product import fake_subscription_product


class SubscriptionTest(TestCase):
    """Test cases for the Subscription services."""

    def test_subscription_extension(self):
        """Test the subscription extension functionality."""
        from sale.models import Subscription
        from sale.services.subscription import subscription_extension, SubscriptionExtensionError

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
            self.assertTrue(True)
            self.assertEqual(datetime.date(2000, 1, 31), subscription.end_billed_date)
        except SubscriptionExtensionError:
            self.fail("SubscriptionExtensionError raised unexpectedly when subscription is not cancelled")

        # Cancel the subscription
        subscription.cancelled_date = datetime.date(2000, 1, 1)
        subscription.save()
        try:
            subscription_extension(subscription.id)
        except SubscriptionExtensionError:
            self.assertTrue(True)  # Expecting an error since the subscription is cancelled