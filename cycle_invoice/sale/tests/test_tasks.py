"""Tests for sale tasks."""
import datetime

from dateutil.relativedelta import relativedelta
from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.sale.tasks import subscription_processing_to_document_items
from cycle_invoice.sale.tests.models.test_subscription import fake_subscription


class TasksTest(TestCase):
    """Test case for sale tasks."""

    def test_subscription_processing_to_document_items(self) -> None:
        """
        Test the subscription processing task.

        This test checks if the task runs without errors.
        It does not check the actual processing logic, which should be tested separately.
        """
        user = get_default_test_user()
        today = datetime.datetime.now(tz=datetime.UTC).date()

        subscription1 = fake_subscription(save=False)
        subscription1.start_date = today
        subscription1.end_billed_date = today
        subscription1.save(user=user)

        subscription2 = fake_subscription(save=False)
        subscription2.start_date = today
        subscription2.end_billed_date = today + relativedelta(months=1)
        subscription2.save(user=user)

        subscription_processing_to_document_items.apply()

        subscription1.refresh_from_db()
        subscription2.refresh_from_db()
        self.assertEqual(today + relativedelta(months=1), subscription1.end_billed_date)
        self.assertEqual(today + relativedelta(months=1), subscription2.end_billed_date)
