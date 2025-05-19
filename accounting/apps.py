"""Accounting app configuration module."""

from django.apps import AppConfig


class AccountingConfig(AppConfig):
    """Configuration class for the accounting app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounting"

    def ready(self) -> None:
        """Call to import signals."""
        from . import signals  # noqa: F401
