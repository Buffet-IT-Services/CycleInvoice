"""Tests for common models."""
from unittest.mock import MagicMock

from django.contrib.auth.models import User
from django.test import TestCase

from cycle_invoice.common.models import BaseModelAdmin, TestBaseModel


class TestBaseModelTest(TestCase):
    """Tests for the TestBaseModel model."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")

    def test_str(self) -> None:
        """Test the string representation of the model."""
        instance = TestBaseModel(
            name="Test Model",
        )
        self.assertEqual(str(instance), "Test Model")

    def test_save_sets_created_by_and_updated_by(self) -> None:
        """Test that save sets created_by and updated_by fields."""
        instance = TestBaseModel(name="Test Save")
        instance.save(user=self.user1)
        self.assertEqual(instance.created_by, self.user1)
        self.assertEqual(instance.updated_by, self.user1)

    def test_save_updates_updated_by(self) -> None:
        """Test that save updates updated_by field."""
        instance = TestBaseModel(name="Test Update")
        instance.save(user=self.user1)
        instance.name = "Updated Name"
        instance.save(user=self.user2)
        self.assertEqual(instance.created_by, self.user1)
        self.assertEqual(instance.updated_by, self.user2)

    def test_save_without_user_raises(self) -> None:
        """Test that save raises ValueError if user is not provided."""
        instance = TestBaseModel(name="No User")
        with self.assertRaises(ValueError):
            instance.save()

    def test_soft_delete_sets_flag_and_updated_by(self) -> None:
        """Test that soft delete sets soft_deleted flag and updated_by."""
        instance = TestBaseModel(name="Soft Delete")
        instance.save(user=self.user1)
        instance.delete(user=self.user2)
        instance.refresh_from_db()
        self.assertTrue(instance.soft_deleted)
        self.assertEqual(instance.updated_by, self.user2)

    def test_delete_without_user_raises(self) -> None:
        """Test that delete raises ValueError if user is not provided."""
        instance = TestBaseModel(name="No User Delete")
        instance.save(user=self.user1)
        with self.assertRaises(ValueError):
            instance.delete()

    def test_hard_delete_removes_instance(self) -> None:
        """Test that hard delete removes the instance from the database."""
        instance = TestBaseModel(name="Hard Delete")
        instance.save(user=self.user1)
        pk = instance.pk
        instance.delete(user=self.user1, hard_delete=True)
        self.assertFalse(TestBaseModel.objects.filter(pk=pk).exists())


class TestBaseModelAdminTest(TestCase):
    """Tests for the BaseModelAdmin class."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create(username="user1")

    def test_admin_save_model_sets_user(self) -> None:
        """Test that the admin save_model sets the user correctly."""
        admin = BaseModelAdmin(TestBaseModel, None)
        request = MagicMock()
        request.user = self.user
        obj = TestBaseModel(name="Admin Save")
        admin.save_model(request, obj, form=None, change=False)
        self.assertEqual(obj.created_by, self.user)
        self.assertEqual(obj.updated_by, self.user)
