"""Admin configuration for the vehicle app."""

from django.apps import AppConfig


class VehicleConfig(AppConfig):
    """Configuration for the vehicle app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "vehicle"
