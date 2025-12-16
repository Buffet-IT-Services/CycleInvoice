"""Models for the accounting app."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from cycle_invoice.common.models import BaseModel
from cycle_invoice.common.system import get_system_user


class Account(BaseModel):
    """Model representing an account."""

    name = models.CharField(
        _("name"),
        max_length=255,
        unique=True
    )
    number = models.CharField(
        _("account number"),
        max_length=20,
        unique=True
    )

    def __str__(self) -> str:
        """Return a string representation of the account."""
        return f"{self.name} ({self.number})"


def get_default_buy_account() -> int:
    """Retrieve the ID of the account with default_buy set to True."""
    try:
        return Account.objects.get(default_buy=True).id
    except Account.DoesNotExist:
        # Create the default account
        account = Account(
            name="Default Buy Account",
            number="sys0001",
            default_buy=True,
        )
        account.save(user=get_system_user())
        return account.id


def get_default_sell_account() -> int:
    """Retrieve the ID of the account with default_sell set to True."""
    try:
        return Account.objects.get(default_sell=True).id
    except Account.DoesNotExist:
        # Create the default account
        account = Account(
            name="Default Sell Account",
            number="sys0002",
            default_sell=True,
        )
        account.save(user=get_system_user())
        return account.id


class Transaction(BaseModel):
    """Model representing a transaction."""

    date = models.DateField(
        _("transaction date"),
        auto_now_add=True
    )
    account_from = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions_from",
        verbose_name=_("account from"),
    )
    account_to = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions_to",
        verbose_name=_("account to"),
    )
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("amount")
    )