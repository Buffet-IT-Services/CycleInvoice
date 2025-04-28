"""A module for sale models."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from recurring.models import RecurrenceRule

from accounting.models import Account, get_default_account_buy, get_default_account_sell
from common.models import ChangeLoggerAll


class Product(ChangeLoggerAll):
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
    subscription_only = models.BooleanField(verbose_name=_("subscription only"), default=False)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency="CHF", verbose_name=_("price"))

    class Meta:
        """Meta options for the Product model."""

        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        """Return a string representation of the SaleProduct."""
        return self.name


class Subscription(ChangeLoggerAll):
    """Model representing a subscription."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="subscriptions")
    price = MoneyField(max_digits=14, decimal_places=2, default_currency="CHF", verbose_name=_("price"))
    recurrence = models.ForeignKey(RecurrenceRule, on_delete=models.CASCADE, related_name="recurrences")

    class Meta:
        """Meta options for the Subscription model."""

        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
