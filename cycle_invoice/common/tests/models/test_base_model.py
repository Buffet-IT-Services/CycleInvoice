"""Tests for the common model BaseModel."""

from django.test import TestCase

from cycle_invoice.common.models import BaseModel, User
from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.common.tests.factories import UserFactory


class TestBaseModel(TestCase):
    """Tests for the common model BaseModel."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.user = get_system_user()
        self.user1 = UserFactory.create()
        self.user2 = UserFactory.create()
        self.user2.delete(user=self.user)

    def test_base_model_active_manager_default(self) -> None:
        """Active manager should exclude soft-deleted objects."""
        qs_active = User.objects.filter()
        self.assertIn(self.user1, qs_active)
        self.assertNotIn(self.user2, qs_active)

    def test_base_model_active_manager_including_deleted(self) -> None:
        """Active manager with deleted should include soft-deleted objects."""
        qs_with_deleted = User.objects_with_deleted.filter()
        self.assertIn(self.user1, qs_with_deleted)
        self.assertIn(self.user2, qs_with_deleted)

    def test_base_model_active_query_set_active(self) -> None:
        """active() should return only not soft-deleted objects."""
        qs = BaseModel.ActiveQuerySet(model=User)

        active_qs = qs.active()
        self.assertIn(self.user1, active_qs)
        self.assertNotIn(self.user2, active_qs)

    def test_base_model_save_rejects_deleted(self) -> None:
        """save() should reject soft-deleted objects."""
        with self.assertRaises(ValueError):
            self.user2.save(user=self.user)

    def test_base_model_save_user_is_required(self) -> None:
        """save() should raise an error if a user is not provided."""
        with self.assertRaises(ValueError):
            self.user1.save()

    def test_base_model_allow_save_for_active(self) -> None:
        """save() should allow active objects."""
        self.user1.save(user=self.user)
        self.assertEqual(self.user1.pk, User.objects.get(pk=self.user1.pk).pk)

    def test_base_model_delete_hard_deletes(self) -> None:
        """delete() should hard delete objects when hard_delete=True."""
        self.user2.delete(user=self.user, hard_delete=True)
        self.assertFalse(User.objects.filter(pk=self.user2.pk).exists())

    def test_base_model_delete_soft_deletes(self) -> None:
        """delete() should soft-delete objects when hard_delete=False."""
        self.user2.delete(user=self.user)
        self.assertTrue(User.objects_with_deleted.filter(pk=self.user2.pk).exists())

    def test_base_model_delete_user_is_required(self) -> None:
        """delete() should raise an error if a user is not provided."""
        with self.assertRaises(ValueError):
            self.user2.delete()

    def test_base_model_recover_recovers(self) -> None:
        """recover() should recover a soft-deleted object."""
        self.user2.delete(user=self.user)
        self.user2.recover(user=self.user)
        self.assertTrue(User.objects.filter(pk=self.user2.pk).exists())

    def test_base_model_recover_raises_error_for_active(self) -> None:
        """recover() should raise an error for an active object."""
        with self.assertRaises(ValueError):
            self.user1.recover(user=self.user)
