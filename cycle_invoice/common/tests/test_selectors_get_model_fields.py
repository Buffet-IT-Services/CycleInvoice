"""Tests for the common selector method get_model_fields(instance: models.Model) -> dict[str, models.Field]."""

from django.test import TestCase

from cycle_invoice.common.models import User
from cycle_invoice.common.selectors import get_model_fields


class TestSelectorsGetModelFields(TestCase):
    """Tests for selector method get_model_fields(instance: models.Model) -> dict[str, models.Field]."""

    def test_get_model_fields(self) -> None:
        """Test get_model_fields() with a normal model."""
        user = User.objects.create(email="")
        return_value = get_model_fields(user)
        self.assertIn("email", return_value)
        self.assertIn("first_name", return_value)
        self.assertIn("last_name", return_value)
        self.assertIn("is_active", return_value)
        self.assertIn("is_staff", return_value)
        self.assertIn("is_superuser", return_value)

    def test_get_model_fields_idempotence(self) -> None:
        """Test get_model_fields() idempotence."""
        user1 = User.objects.create(email="1")
        user2 = User.objects.create(email="2")
        return_value1 = get_model_fields(user1)
        return_value2 = get_model_fields(user2)
        self.assertEqual(return_value1, return_value2)
