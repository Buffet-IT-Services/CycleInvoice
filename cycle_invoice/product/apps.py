"""Config for the product app."""
from django.apps import AppConfig


class ProductConfig(AppConfig):
    """Config for the product app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cycle_invoice.product'
