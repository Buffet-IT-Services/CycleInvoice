"""Validators for the accounting application."""

from django.core.exceptions import ValidationError


def validate_account_exists(value: int) -> bool:
    """Validate that the account exists in the database."""
    from .models import Account

    try:
        Account.objects.get(number=value)
    except Account.DoesNotExist:
        msg = f"Account '{value}' does not exist"
        raise ValidationError(msg) from Account.DoesNotExist
    else:
        return True
