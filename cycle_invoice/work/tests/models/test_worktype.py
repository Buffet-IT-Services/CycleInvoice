"""Tests for the work model WorkType."""

from django.test import TestCase

from cycle_invoice.work.tests.factories import WorkTypeFactory


class TestWorkType(TestCase):
    """Tests for the work model WorkType."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.work_type = WorkTypeFactory.create()

    def test_worktype_str(self) -> None:
        """Test WorkType.__str__()."""
        self.assertEqual(f"{self.work_type.name} - {self.work_type.price_per_hour}", str(self.work_type))
