"""Models for the accounting app."""
from django.core.exceptions import ValidationError
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
        constraints = [
            models.CheckConstraint(
                check=~(models.Q(soft_deleted=True) & (models.Q(default_buy=True) | models.Q(default_sell=True))),
                name="%(app_label)s_%(class)s_prevent_soft_delete_if_default_buy_or_sell",
            ),
        ]

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
            # Check if this account is the current default_sell account
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


class Payment(Transaction):
    """Model representing a payment transaction."""

    payment_method = models.CharField(max_length=50, verbose_name=_("payment method"))
    invoice = models.ForeignKey("sale.DocumentInvoice", on_delete=models.CASCADE,
                                verbose_name=_("invoice"))

    class Meta:
        """Meta options for the Payment model."""

        verbose_name = "Payment"
        verbose_name_plural = "Payments"
