"""Tests for the subscription model SubscriptionPlan."""

from django.test import TestCase

from cycle_invoice.subscription.tests.factories import SubscriptionPlanFactory


class TestSubscriptionPlan(TestCase):
    """Tests for the subscription model SubscriptionPlan."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.subscription_plan = SubscriptionPlanFactory.create()

    def test_subscriptionplan_str(self) -> None:
        """Test SubscriptionPlan.__str__()."""
        self.assertEqual(f"{self.subscription_plan.product.name} - Yearly", str(self.subscription_plan))
