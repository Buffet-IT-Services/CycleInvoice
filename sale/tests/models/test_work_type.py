"""Test cases for the WorkType model."""

from django.test import TestCase

from accounting.tests.models.test_account import fake_account
from sale.models import WorkType


def fake_work_type() -> WorkType:
    """Create a fake work type."""
    return WorkType.objects.create(name="Test Work Type", account=fake_account())

class WorkTypeTest(TestCase):
    """Test cases for the WorkType model."""

    def test_str(self) -> None:
        self.assertEqual("Test Work Type", str(fake_work_type()))
