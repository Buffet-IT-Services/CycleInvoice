"""App configuration for the common app."""

from django.apps import AppConfig


class CommonConfig(AppConfig):
    """App configuration for the common app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "common"
