"""A module for sale models."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from accounting.models import Account, get_default_account_buy, get_default_account_sell
from common.models import ChangeLoggerAll


class SaleProduct(ChangeLoggerAll):
    """Model representing a sale product."""

    name = models.CharField(_("name"), max_length=255)
    account_buy = models.ForeignKey(
        Account,
        on_delete=models.SET_DEFAULT,
        default=get_default_account_buy,
        related_name="sale_product_buy_account",
    )
    account_sell = models.ForeignKey(
        Account,
        on_delete=models.SET_DEFAULT,
        default=get_default_account_sell,
        related_name="sale_products_sell_account",
    )

    class Meta:
        """Meta options for the SaleProduct model."""

        verbose_name = "Sale Item"
        verbose_name_plural = "Sale Items"

    def __str__(self) -> str:
        """Return a string representation of the SaleProduct."""
        return self.name


class SubscriptionItem(ChangeLoggerAll):
    """Model representing a subscription."""

    start_date = models.DateField(_("start date"))
    billed_until = models.DateField(_("billed until"), null=True, blank=True)

    class Meta:
        """Meta options for the Subscription model."""

        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
