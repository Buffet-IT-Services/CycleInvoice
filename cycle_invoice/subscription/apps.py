"""Application configuration for the subscription app."""
from django.apps import AppConfig


class SubscriptionConfig(AppConfig):
    """Configuration for the subscription app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cycle_invoice.subscription'
