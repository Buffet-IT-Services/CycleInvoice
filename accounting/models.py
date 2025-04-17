"""A module for accounting models."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import ChangeLoggerAll


class Account(ChangeLoggerAll):
    """Model representing an account."""

    name = models.CharField(_("name"), max_length=255, unique=True)
    number = models.CharField(_("account number"), max_length=20, unique=True)

    class Meta:
        """Meta options for the Account model."""

        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self) -> str:
        """Return a string representation of the account."""
        return f"{self.name} ({self.number})"


def get_default_account_buy() -> Account:
    """Get the default account for buying."""
    account, created = Account.objects.get_or_create(
        number=4000,
        defaults={"name": "Default Account Buy"},
    )
    return account


def get_default_account_sell() -> Account:
    """Get the default account for selling."""
    account, created = Account.objects.get_or_create(
        number=3000,
        defaults={"name": "Default Account Sell"},
    )
    return account
