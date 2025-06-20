"""App Config for the work app."""
from django.apps import AppConfig


class WorkConfig(AppConfig):
    """Configuration for the work app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "cycle_invoice.work"
