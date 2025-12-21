"""Tests for the common model BaseModelAdmin."""

from unittest.mock import Mock

from django.contrib import admin
from django.db.models.query import QuerySet
from django.test import RequestFactory, TestCase

from cycle_invoice.common.models import BaseModelAdmin, User
from cycle_invoice.common.selectors import get_system_user


class TestModelsBaseModelAdmin(TestCase):
    """Tests for the common model BaseModelAdmin."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.user = get_system_user()
        self.admin = BaseModelAdmin(User, admin.site)

        rf = RequestFactory()
        self.request = rf.get("/")

        self.request.user = self.user

    def test_save_model_calls_save_with_user(self) -> None:
        """save_model should call obj.save(user=request.user)."""
        obj = Mock()
        self.admin.save_model(self.request, obj, form=Mock(), change=True)
        obj.save.assert_called_once_with(user=self.request.user)

    def test_delete_model_calls_delete_with_user(self) -> None:
        """delete_model should call obj.delete(user=request.user)."""
        obj = Mock()
        self.admin.delete_model(self.request, obj)
        obj.delete.assert_called_once_with(user=self.request.user)

    def test_soft_delete_selected_calls_delete_for_each(self) -> None:
        """soft_delete_selected action should call delete for every obj in the queryset."""
        objs = [Mock(), Mock(), Mock()]
        queryset_mock = Mock(spec=QuerySet)
        queryset_mock.__iter__ = lambda _=None: iter(objs)

        self.admin.soft_delete_selected(self.request, queryset_mock)
        for o in objs:
            o.delete.assert_called_once_with(user=self.request.user)

    def test_action_registered(self) -> None:
        """Ensure the admin action is registered on the admin instance."""
        self.assertIn("soft_delete_selected", getattr(self.admin, "actions", []))
