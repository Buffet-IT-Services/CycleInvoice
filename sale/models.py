"""A module for sale models."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from accounting.models import Account, get_default_account_buy, get_default_account_sell
from common.models import ChangeLoggerAll


class SaleItem(ChangeLoggerAll):
    """Model representing a sale item."""

    name = models.CharField(_("name"), max_length=255)
    account_buy = models.ForeignKey(
        Account,
        on_delete=models.SET_DEFAULT,
        default=get_default_account_buy,
        related_name="sale_items_buy_account",
    )
    account_sell = models.ForeignKey(
        Account,
        on_delete=models.SET_DEFAULT,
        default=get_default_account_sell,
        related_name="sale_items_sell_account",
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=[
            ("draft", _("Draft")),
            ("open", _("Open")),
            ("billed", _("Billed")),
        ],
        default="draft",
    )

    class Meta:
        """Meta options for the SaleItem model."""

        verbose_name = "Sale Item"
        verbose_name_plural = "Sale Items"

    def __str__(self) -> str:
        """Return a string representation of the sale item."""
        return self.name
