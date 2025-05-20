"""Test cases for the WorkTypePrice model."""

from django.test import TestCase

from sale.models import WorkType, WorkTypePrice
from sale.tests.models.test_work_type import fake_work_type


def fake_work_type_price() -> WorkTypePrice:
    """Create a fake work type price."""
    return WorkTypePrice.objects.create(work_type=fake_work_type(), price=100.0)

class WorkTypePriceTest(TestCase):
    """Test cases for the WorkTypePrice model."""

    def test_str(self) -> None:
        self.assertEqual("Test Work Type - 100.00", str(fake_work_type_price()))
