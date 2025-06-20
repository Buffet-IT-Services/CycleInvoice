"""Test cases for the WorkType model."""

from django.test import TestCase

from cycle_invoice.accounting.tests.models.test_account import fake_account
from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.sale.models import WorkType


def fake_work_type(save: bool) -> WorkType:
    """Create a fake work type."""
    work_type = WorkType(
        name="Test Work Type",
        account=fake_account(save=True),
        price_per_hour=100.0
    )
    if save:
        work_type.save(user=get_default_test_user())
    return work_type


class WorkTypeTest(TestCase):
    """Test cases for the WorkType model."""

    def test_str(self) -> None:
        """Test the string representation of the WorkType model."""
        self.assertEqual("Test Work Type - 100.00", str(fake_work_type(save=False)))
