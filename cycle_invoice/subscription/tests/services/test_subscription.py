"""Tests for the subscription service Subscription."""
from datetime import datetime

from django.test import TestCase

from cycle_invoice.common.models import DiscountType
from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.subscription.models import SubscriptionDocumentItem
from cycle_invoice.subscription.services.subscription import SubscriptionExtensionError, subscription_extension
from cycle_invoice.subscription.tests.factories import SubscriptionFactory


class TestSubscription(TestCase):
    """Tests behavior of the subscription_extension service function."""

    def setUp(self) -> None:
        """Create a normal subscription and a canceled subscription used by tests."""
        self.subscription = SubscriptionFactory.create()
        self.subscription_cancelled = SubscriptionFactory.create(
            cancelled_date=datetime.now(tz=datetime.timezone.utc).date())

    def test_subscription_extension_block_cancelled(self) -> None:
        """Assert extending a canceled subscription raises SubscriptionExtensionError."""
        with self.assertRaises(SubscriptionExtensionError):
            subscription_extension(subscription_id=self.subscription_cancelled.id, user=get_system_user())

    def test_subscription_extension_creates_correct(self) -> None:
        """Extend a subscription and assert dates change, and a correct SubscriptionDocumentItem is created."""
        start = self.subscription.next_start_billed_date
        end = self.subscription.next_end_billed_date
        time_range = f"{start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}"
        subscription_extension(subscription_id=self.subscription.id, user=get_system_user())
        self.subscription.refresh_from_db()
        self.assertNotEqual(start, self.subscription.next_start_billed_date)
        self.assertNotEqual(end, self.subscription.next_end_billed_date)

        subscription_document_item = SubscriptionDocumentItem.objects.get(subscription=self.subscription)
        self.assertEqual(subscription_document_item.price, self.subscription.plan.price)
        self.assertEqual(subscription_document_item.quantity, 1)
        self.assertIsNone(subscription_document_item.document)
        self.assertEqual(subscription_document_item.title, f"{self.subscription.plan.product.name} - {time_range}")
        self.assertEqual(subscription_document_item.description, self.subscription.plan.product.description)
        self.assertEqual(subscription_document_item.party, self.subscription.party)
        self.assertEqual(subscription_document_item.account, self.subscription.plan.product.account_sell)
        self.assertEqual(subscription_document_item.discount_value, 0)
        self.assertEqual(subscription_document_item.discount_type, DiscountType.PERCENT)
        self.assertEqual(subscription_document_item.subscription, self.subscription)

    def test_subscription_extension_no_user(self) -> None:
        """Assert subscription_extension raises ValueError when no user is provided."""
        with self.assertRaises(ValueError):
            subscription_extension(subscription_id=self.subscription.id, user=None)

    def test_subscription_extension_invalid_subscription(self) -> None:
        """Assert subscription_extension raises ValueError for a non-existent subscription id."""
        with self.assertRaises(ValueError):
            subscription_extension(subscription_id=999999, user=get_system_user())
