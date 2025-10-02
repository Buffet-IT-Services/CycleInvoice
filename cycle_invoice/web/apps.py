"""Application configuration for the web app."""

from django.apps import AppConfig


class WebConfig(AppConfig):
    """Configuration for the web app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "cycle_invoice.web"
