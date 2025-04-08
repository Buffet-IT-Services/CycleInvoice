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
        return self.name


def get_default_account_buy() -> Account:
    """Get the default account for buying."""
    return Account.objects.get(number="4000") if Account.objects.filter(number="4000").exists() else None


def get_default_account_sell() -> Account:
    """Get the default account for buying."""
    return Account.objects.get(number="3000") if Account.objects.filter(number="3000").exists() else None
