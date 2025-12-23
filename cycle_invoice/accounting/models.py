"""Models for the accounting app."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from cycle_invoice.common.models import BaseModel


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
