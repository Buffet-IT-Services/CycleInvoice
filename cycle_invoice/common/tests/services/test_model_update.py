"""Tests for the common service method model_update()."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import TestCase

from cycle_invoice.common.services import model_update
from cycle_invoice.common.tests.factories import UserFactory

if TYPE_CHECKING:
    from cycle_invoice.common.models import User


class TestModelUpdate(TestCase):
    """Tests for the common service method model_update()."""

    def setUp(self) -> None:
        """Create a target instance and an acting user for updates."""
        self.instance: User = UserFactory.create()
        self.updated_at = self.instance.updated_at
        self.updated_by = self.instance.updated_by
        self.actor: User = UserFactory.create()

    def test_model_update_soft_deleted(self) -> None:
        """Test model_update() with a soft-deleted instance."""
        local_instance = UserFactory.create(soft_deleted=True)
        self.assertRaises(
            ValueError, model_update, local_instance, ["first_name"], {"first_name": "NewName"}, self.actor)

    def test_model_update_no_fields(self) -> None:
        """Test model_update() with no changes."""
        model_update(self.instance, [], {}, self.actor)
        self.assertEqual(self.updated_at, self.instance.updated_at)
        self.assertEqual(self.updated_by, self.instance.updated_by)

    def test_model_update_no_data(self) -> None:
        """Test model_update() with data changes."""
        model_update(self.instance, ["first_name"], {}, self.actor)
        self.assertEqual(self.updated_at, self.instance.updated_at)
        self.assertEqual(self.updated_by, self.instance.updated_by)

    def test_model_update_same_data(self) -> None:
        """Test model_update() with the same fields."""
        model_update(self.instance, ["first_name"], {"first_name": self.instance.first_name}, self.actor)
        self.assertEqual(self.updated_at, self.instance.updated_at)
        self.assertEqual(self.updated_by, self.instance.updated_by)

    def test_model_update_wrong_field(self) -> None:
        """Test model_update() with a wrong field."""
        self.assertRaises(
            ValueError, model_update, self.instance, ["wrong_field"], {"wrong_field": "NewName"}, self.actor)
        self.assertEqual(self.updated_at, self.instance.updated_at)
        self.assertEqual(self.updated_by, self.instance.updated_by)

    def test_model_update_no_actor(self) -> None:
        """Test model_update() with no actor."""
        self.assertRaises(
            ValueError, model_update, self.instance, ["first_name"], {"first_name": "New First"}, None)

    def test_model_update_actor_not_in_db(self) -> None:
        """Test model_update() with an actor not in the database."""
        actor = UserFactory.build()
        self.assertRaises(ValueError, model_update, self.instance, ["first_name"], {"first_name": "New First"}, actor)
