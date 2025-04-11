"""Accounting app configuration module."""

from django.apps import AppConfig


class AccountingConfig(AppConfig):
    """Configuration class for the accounting app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounting"
