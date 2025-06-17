"""Test cases for the WorkType model."""

from django.test import TestCase

from cycle_invoice.accounting.tests.models.test_account import fake_account
from cycle_invoice.sale.models import WorkType


def fake_work_type() -> WorkType:
    """Create a fake work type."""
    return WorkType.objects.create(name="Test Work Type", account=fake_account(), price_per_hour=100.0)


class WorkTypeTest(TestCase):
    """Test cases for the WorkType model."""

    def test_str(self) -> None:
        """Test the string representation of the WorkType model."""
        self.assertEqual("Test Work Type - 100.00", str(fake_work_type()))
