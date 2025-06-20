"""Tests for common services."""
from django.test import TestCase

from cycle_invoice.common.models import TestBaseModel
from cycle_invoice.common.services import get_model_fields, model_update
from cycle_invoice.common.tests.base import get_default_test_user


class ModelUpdateTest(TestCase):
    """Tests for the model_update service."""

    def setUp(self) -> None:
        """Set up the test case with a default user and an instance of TestBaseModel."""
        self.user = get_default_test_user()
        self.new_user = get_default_test_user(username="otheruser")
        self.instance = TestBaseModel()
        self.instance.save(user=self.user)

    def test_update_field(self) -> None:
        """Test updating a single field."""
        instance, updated = model_update(
            instance=self.instance,
            fields=["name"],
            data={"name": "New Name"},
            user=self.new_user,
        )
        self.assertTrue(updated)
        self.assertEqual(instance.name, "New Name")
        self.assertEqual(instance.updated_by, self.new_user)
        self.assertNotEqual(instance.updated_at, instance.created_at)

    def test_no_update_when_same_value(self) -> None:
        """Test that no update occurs when the value is the same."""
        updated_time = self.instance.updated_at
        instance, updated = model_update(
            instance=self.instance,
            fields=["name"],
            data={"name": ""},
            user=self.new_user,
        )
        self.assertFalse(updated)
        self.assertEqual(instance.name, "")
        self.assertEqual(instance.updated_by, self.user)
        self.assertEqual(instance.updated_at, updated_time)

    def test_update_with_field_without_value(self) -> None:
        """Test updating a field with an empty value."""
        updated_time = self.instance.updated_at
        instance, updated = model_update(
            instance=self.instance,
            fields=["name"],
            data={"other_field": "Some Value"},
            user=self.new_user,
        )
        self.assertFalse(updated)
        self.assertEqual(instance.name, "")
        self.assertEqual(instance.updated_by, self.user)
        self.assertEqual(instance.updated_at, updated_time)

    def test_invalid_field_raises(self) -> None:
        """Test that an invalid field raises an AssertionError."""
        with self.assertRaises(AssertionError):
            model_update(
                instance=self.instance,
                fields=["not_a_field"],
                data={"not_a_field": 123},
                user=self.user,
            )

    def test_with_user_none(self) -> None:
        """Test updating without passing a user."""
        with self.assertRaises(ValueError):
            model_update(
                instance=self.instance,
                fields=["name"],
                data={"name": "No User Update"},
                user=None,
            )

class GetModelFields(TestCase):
    """Tests for the get_model_fields service."""

    def test_get_model_fields(self) -> None:
        """Test retrieving model fields."""
        fields = get_model_fields(TestBaseModel())
        self.assertIsInstance(fields, dict)
        self.assertIn("id", fields)
        self.assertIn("name", fields)
        self.assertIn("uuid", fields)
        self.assertIn("created_at", fields)
        self.assertIn("updated_at", fields)
        self.assertIn("created_by", fields)
        self.assertIn("updated_by", fields)
        self.assertIn("soft_deleted", fields)
        self.assertEqual(len(fields), 8)  # Adjust based on actual model fields
