"""Signals for the accounting app."""

from django.core.exceptions import ValidationError
from django.db.models import Model
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from cycle_invoice.accounting.models import Account


# noinspection PyUnusedLocal,PyUnresolvedReferences
@receiver(pre_delete, sender=Account)
def prevent_default_account_deletion(sender: Model, instance: Model, **kwargs) -> None:  # noqa: ARG001
    """Prevents the deletion of default accounts."""
    if instance.default_buy or instance.default_sell:
        msg = "Cannot delete this account as it is set as the default for buy or sell."
        raise ValidationError(msg)
