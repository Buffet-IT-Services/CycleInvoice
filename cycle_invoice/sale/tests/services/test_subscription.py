"""Test cases for the Subscription services."""

import datetime

from django.test import TestCase

from cycle_invoice.contact.tests.models.test_contact import fake_contact
from cycle_invoice.sale.models import DocumentItem, Subscription
from cycle_invoice.sale.services.subscription import SubscriptionExtensionError, subscription_extension
from cycle_invoice.sale.tests.models.test_subscription_product import fake_subscription_product


class SubscriptionTest(TestCase):
    """Test cases for the Subscription services."""

    def test_subscription_extension_valid(self) -> None:
        """Test the subscription extension functionality."""
        # Create a subscription
        subscription = Subscription.objects.create(
            product=fake_subscription_product(),
            customer=fake_contact(),
            start_date=datetime.date(2000, 1, 1),
        )

        try:
            subscription_extension(subscription.id)
            subscription.refresh_from_db()
            self.assertEqual(datetime.date(2000, 1, 31), subscription.end_billed_date)
            subscription_item = DocumentItem.objects.get(subscription=subscription)
            self.assertEqual(subscription, subscription_item.subscription)
            self.assertEqual("01.01.2000 - 31.01.2000", subscription_item.comment_title)
            self.assertEqual(subscription.product.product, subscription_item.product)
            self.assertEqual(subscription.product.price, subscription_item.price)
            self.assertEqual(1, subscription_item.quantity)
            self.assertEqual(0, subscription_item.discount)
            self.assertEqual(subscription.customer, subscription_item.customer)
        except SubscriptionExtensionError:
            self.fail("SubscriptionExtensionError raised unexpectedly when subscription is not cancelled")

    def test_subscription_extension_cancelled(self) -> None:
        """Test the subscription extension functionality with a cancelled subscription."""
        subscription = Subscription.objects.create(
            product=fake_subscription_product(),
            customer=fake_contact(),
            start_date=datetime.date(2000, 1, 1),
            cancelled_date=datetime.date(2000, 1, 15),
        )

        try:
            subscription_extension(subscription.id)
            self.fail("SubscriptionExtensionError doesn't raise when subscription is cancelled")
        except SubscriptionExtensionError:
            self.assertTrue(subscription.is_cancelled)
