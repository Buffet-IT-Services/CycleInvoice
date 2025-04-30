"""A module for accounting models."""
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from extra_settings.models import Setting
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

    def delete(self, *args, **kwargs):
        """
        Override the delete method to prevent deletion of default accounts.
        :param args:
        :param kwargs:
        """
        default_account_buy = Setting.get("ACCOUNTING_DEFAULT_ACCOUNT_BUY")
        default_account_sell = Setting.get("ACCOUNTING_DEFAULT_ACCOUNT_SELL")

        if str(self.number) == str(default_account_buy) or str(self.number) == str(default_account_sell):
            raise ValidationError("This account is set as the default and cannot be deleted.")

        super().delete(*args, **kwargs)
