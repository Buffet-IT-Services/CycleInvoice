"""A module for accounting models."""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import ChangeLoggerAll


class Account(ChangeLoggerAll):
    """Model representing an account."""

    name = models.CharField(_("name"), max_length=255, unique=True)
    number = models.CharField(_("account number"), max_length=20, unique=True)
    default_buy = models.BooleanField(
        _("default buy account"),
        default=False,
        help_text=_("Set this account as the default for buying transactions."),
    )
    default_sell = models.BooleanField(
        _("default sell account"),
        default=False,
        help_text=_("Set this account as the default for selling transactions."),
    )

    class Meta:
        """Meta options for the Account model."""

        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def clean(self) -> None:
        """
        Clean the model.

        Ensures only one account can be set as default for buying and selling and removes the tag from others.
        Prevents removal of default_buy and default_sell if they are the only ones set.
        """
        if self.default_buy:
            Account.objects.filter(default_buy=True).exclude(id=self.id).update(default_buy=False)
        if self.default_sell:
            Account.objects.filter(default_sell=True).exclude(id=self.id).update(default_sell=False)
        if not self.default_buy and self.pk:
            # Check if this account is the current default_buy account
            current_default = Account.objects.filter(pk=self.pk, default_buy=True).exists()
            if current_default:
                raise ValidationError(_("You cannot remove default_buy from this account."))
            if not self.default_sell and self.pk:
                # Check if this account is the current default_buy account
                current_default = Account.objects.filter(pk=self.pk, default_sell=True).exists()
                if current_default:
                    raise ValidationError(_("You cannot remove default_sell from this account."))

    def __str__(self) -> str:
        """Return a string representation of the account."""
        return f"{self.name} ({self.number})"


def get_default_buy_account() -> int:
    """Retrieve the ID of the account with default_buy set to True."""
    try:
        return Account.objects.get(default_buy=True).id
    except Account.DoesNotExist:
        # Create the default account
        account = Account.objects.create(
            name="Default Buy Account",
            number="sys0001",
            default_buy=True,
        )
        return account.id


def get_default_sell_account() -> int:
    """Retrieve the ID of the account with default_sell set to True."""
    try:
        return Account.objects.get(default_sell=True).id
    except Account.DoesNotExist:
        # Create the default account
        account = Account.objects.create(
            name="Default Sell Account",
            number="sys0002",
            default_sell=True,
        )
        return account.id
