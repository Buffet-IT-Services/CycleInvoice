"""Contains signals for the accounting app."""

from django.core.exceptions import ValidationError
from django.db.models import Model
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from accounting.models import Account


@receiver(pre_delete, sender=Account)
def prevent_default_account_deletion(sender: Model, instance: Model, **kwargs) -> None:  # noqa: ARG001
    """Prevents the deletion of default accounts."""
    if instance.default_buy or instance.default_sell:
        msg = "This account is set as the default and cannot be deleted."
        raise ValidationError(msg)
