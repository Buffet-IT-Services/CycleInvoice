"""Management command to ensure a default superuser exists."""
from __future__ import annotations

import os
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from cycle_invoice.common.selectors import get_system_user


class Command(BaseCommand):
    """Create or update a default superuser based on environment variables."""

    help = (
        "Ensures a default superuser exists when DEFAULT_SUPERUSER_EMAIL and "
        "DEFAULT_SUPERUSER_PASSWORD are provided."
    )

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: ARG002
        email = os.getenv("DEFAULT_SUPERUSER_EMAIL")
        password = os.getenv("DEFAULT_SUPERUSER_PASSWORD")

        if not email:
            self.stdout.write(
                self.style.WARNING(
                    "DEFAULT_SUPERUSER_EMAIL not set; skipping default superuser creation.",
                )
            )
            return

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    "DEFAULT_SUPERUSER_PASSWORD not set; skipping default superuser creation.",
                )
            )
            return

        email = email.lower()
        user_model = get_user_model()
        system_user = get_system_user()

        user = user_model.objects.filter(email=email).first()
        if user:
            updates: dict[str, Any] = {}
            if not user.is_staff:
                updates["is_staff"] = True
            if not user.is_superuser:
                updates["is_superuser"] = True
            if not user.is_active:
                updates["is_active"] = True

            if updates:
                user_model.objects.filter(pk=user.pk).update(**updates)

            if not user.check_password(password):
                user.set_password(password)
                user.save(user=system_user)

            self.stdout.write(self.style.SUCCESS(f"Ensured default superuser '{email}'."))
            return

        user_model.objects.create_superuser(
            email=email,
            password=password,
            first_name="Admin",
            last_name="User",
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS(f"Created default superuser '{email}'."))
