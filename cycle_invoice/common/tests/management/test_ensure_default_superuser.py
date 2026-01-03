"""Tests for ensure_default_superuser management command."""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user


class EnsureDefaultSuperuserTests(TestCase):
    """Tests for ensure_default_superuser management command."""

    def setUp(self) -> None:
        """Set up system user for tests."""
        self.system_user = get_system_user()
        self.user_model = get_user_model()

    def test_creates_superuser_when_env_variables_set(self) -> None:
        """Command creates a superuser using provided environment variables."""
        email = "admin@example.com"
        password = "securepass123"
        with self._patched_env(email=email, password=password):
            call_command("ensure_default_superuser")

        user = self.user_model.objects.get(email=email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(password))

    def test_updates_existing_user_and_password(self) -> None:
        """Command upgrades an existing user to superuser and resets password."""
        email = "existing@example.com"
        initial_password = "oldpass123"
        updated_password = "newpass456"

        existing_user = self.user_model.objects.create_user(email=email)
        existing_user.set_password(initial_password)
        existing_user.save(user=self.system_user)

        with self._patched_env(email=email, password=updated_password):
            call_command("ensure_default_superuser")

        user = self.user_model.objects.get(email=email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(updated_password))

    def test_skips_when_env_missing(self) -> None:
        """Command does nothing when required environment variables are missing."""
        existing_superusers = self.user_model.objects.filter(is_superuser=True).count()

        call_command("ensure_default_superuser")

        self.assertEqual(
            self.user_model.objects.filter(is_superuser=True).count(),
            existing_superusers,
        )

    @contextmanager
    def _patched_env(self, *, email: str | None = None, password: str | None = None) -> Generator[None, None, None]:
        """Temporarily set environment variables required by the command."""
        original_email = os.environ.get("DEFAULT_SUPERUSER_EMAIL")
        original_password = os.environ.get("DEFAULT_SUPERUSER_PASSWORD")
        if email is not None:
            os.environ["DEFAULT_SUPERUSER_EMAIL"] = email
        elif "DEFAULT_SUPERUSER_EMAIL" in os.environ:
            del os.environ["DEFAULT_SUPERUSER_EMAIL"]

        if password is not None:
            os.environ["DEFAULT_SUPERUSER_PASSWORD"] = password
        elif "DEFAULT_SUPERUSER_PASSWORD" in os.environ:
            del os.environ["DEFAULT_SUPERUSER_PASSWORD"]

        try:
            yield
        finally:
            if original_email is not None:
                os.environ["DEFAULT_SUPERUSER_EMAIL"] = original_email
            elif "DEFAULT_SUPERUSER_EMAIL" in os.environ:
                del os.environ["DEFAULT_SUPERUSER_EMAIL"]

            if original_password is not None:
                os.environ["DEFAULT_SUPERUSER_PASSWORD"] = original_password
            elif "DEFAULT_SUPERUSER_PASSWORD" in os.environ:
                del os.environ["DEFAULT_SUPERUSER_PASSWORD"]
