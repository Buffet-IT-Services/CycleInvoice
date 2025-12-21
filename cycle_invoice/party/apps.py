"""Contact app configuration."""

from django.apps import AppConfig


class ContactConfig(AppConfig):
    """Contact app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "cycle_invoice.party"
    label = "contact"
