"""Tests for the subscription model Subscription."""
from datetime import UTC, datetime

from dateutil.relativedelta import relativedelta
from django.test import TestCase

from cycle_invoice.subscription.tests.factories import SubscriptionFactory


class TestSubscription(TestCase):
    """Tests for the subscription model Subscription."""

    def setUp(self) -> None:
        """Create a Subscription instance using the factory (not saved)."""
        self.subscription = SubscriptionFactory.build()

    def test_subscription_str(self) -> None:
        """Subscription.__str__ returns '<product name> - <party>'."""
        self.assertEqual(f"{self.subscription.plan.product.name} - {self.subscription.party.__str__()}",
                         str(self.subscription))

    def test_subscription_is_cancelled(self) -> None:
        """is_cancelled is False when cancelled_date is not set."""
        self.assertFalse(self.subscription.is_cancelled)

    def test_subscription_is_cancelled_cancelled(self) -> None:
        """is_cancelled is True when cancelled_date is set today."""
        subscription = SubscriptionFactory.build(cancelled_date=datetime.now(tz=UTC).date())
        self.assertTrue(subscription.is_cancelled)

    def test_subscription_next_start_billed_date_end_billed_unset(self) -> None:
        """If end_billed_date is unset, next_start_billed_date equals start_date."""
        self.assertEqual(self.subscription.next_start_billed_date, self.subscription.start_date)

    def test_subscription_next_start_billed_date_end_billed_set(self) -> None:
        """If end_billed_date is set, next_start_billed_date is the day after end_billed_date."""
        subscription = SubscriptionFactory.build(end_billed_date=datetime.now(tz=UTC).date())
        self.assertEqual(subscription.next_start_billed_date,
                         datetime.now(tz=UTC).date() + relativedelta(days=1))

    def test_subscription_next_end_billed_date_currently_unset(self) -> None:
        """Yearly recurrence, end_billed_date unset -> start_date + 1 year - 1 day."""
        self.assertEqual(self.subscription.next_end_billed_date,
                         self.subscription.start_date + relativedelta(years=1) - relativedelta(days=1))

    def test_subscription_next_end_billed_date_currently_set(self) -> None:
        """Yearly recurrence, end_billed_date set -> end_billed_date + 1 year."""
        subscription = SubscriptionFactory.build(end_billed_date=datetime.now(tz=UTC).date())
        self.assertEqual(subscription.next_end_billed_date,
                         subscription.end_billed_date + relativedelta(years=1))

    def test_subscription_next_end_billed_date_currently_unset_monthly(self) -> None:
        """Monthly recurrence, end_billed_date unset -> start_date + 1 month - 1 day."""
        subscription = SubscriptionFactory.build(plan__recurrence="monthly")
        self.assertEqual(subscription.next_end_billed_date,
                         subscription.start_date + relativedelta(months=1) - relativedelta(days=1))

    def test_subscription_next_end_billed_date_currently_set_monthly(self) -> None:
        """Monthly recurrence, end_billed_date set -> end_billed_date + 1 month."""
        subscription = SubscriptionFactory.build(end_billed_date=datetime.now(tz=UTC).date(),
                                                 plan__recurrence="monthly")
        self.assertEqual(subscription.next_end_billed_date,
                         subscription.end_billed_date + relativedelta(months=1))

    def test_subscription_next_end_billed_date_recurrence_unknown(self) -> None:
        """Accessing next_end_billed_date with unknown recurrence raises ValueError."""
        subscription = SubscriptionFactory.build(plan__recurrence="unknown")
        with self.assertRaises(ValueError):
            subscription.next_end_billed_date  # noqa: B018, as this should throw an error
