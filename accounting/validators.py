"""
Validators for the accounting application.
"""
from django.core.exceptions import ValidationError


def validate_account_exists(value):
    """
    Validate that the account exists in the database.
    """
    from .models import Account

    try:
        Account.objects.get(number=value)
        return True
    except Account.DoesNotExist:
        raise ValidationError(f"Account with ID {value} does not exist.")