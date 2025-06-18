"""Tests for common models."""
from django.test import TestCase

from cycle_invoice.common.models import TestBaseModel


class TestBaseModelTest(TestCase):
    """Tests for the TestBaseModel model."""

    def test_str(self) -> None:
        """Test the string representation of the model."""
        instance = TestBaseModel(
            name="Test Model",
        )
        self.assertEqual(str(instance), "Test Model")
