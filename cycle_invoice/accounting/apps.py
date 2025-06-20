"""Config for the accounting app."""

from django.apps import AppConfig


class AccountingConfig(AppConfig):
    """Configuration class for the accounting app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "cycle_invoice.accounting"
    label = "accounting"

    def ready(self) -> None:
        """Call to import signals."""
        from . import signals  # noqa: PLC0415,F401
