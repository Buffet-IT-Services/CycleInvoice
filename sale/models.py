"""A module for sale models."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from recurring.models import CalendarEntry

from accounting.models import Account, get_default_buy_account, get_default_sell_account
from common.models import ChangeLoggerAll


class Product(ChangeLoggerAll):
    """Model representing a sale product."""

    name = models.CharField(_("name"), max_length=255)
    account_buy = models.ForeignKey(
        Account,
        on_delete=models.SET_DEFAULT,
        default=get_default_buy_account,
        related_name="sale_product_buy_account",
    )
    account_sell = models.ForeignKey(
        Account,
        on_delete=models.SET_DEFAULT,
        default=get_default_sell_account,
        related_name="sale_products_sell_account",
    )
    price = models.DecimalField(max_digits=14, decimal_places=2, verbose_name=_("price"), null=True, blank=True)

    class Meta:
        """Meta options for the Product model."""

        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        """Return a string representation of the SaleProduct."""
        return self.name


class SubscriptionProduct(ChangeLoggerAll):
    """Model representing a subscription."""

    RECURRENCE_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="subscriptionproduct")
    price = models.DecimalField(max_digits=14, decimal_places=2, verbose_name=_("price"))
    recurrence = models.CharField(
        max_length=10,
        choices=RECURRENCE_CHOICES,
        default="yearly",
    )

    class Meta:
        """Meta options for the Subscription model."""

        verbose_name = "Subscription Product"
        verbose_name_plural = "Subscription Products"

    def __str__(self) -> str:
        """Return a string representation of the Subscription."""
        return f"{self.product.name} - {self.recurrence}"


class Subscription(ChangeLoggerAll):
    """Model representing a subscription."""

    product = models.ForeignKey(SubscriptionProduct, on_delete=models.CASCADE, related_name="subscription")
    customer = models.ForeignKey("contact.Customer", on_delete=models.CASCADE, related_name="subscription")
    calendar_entry = models.ForeignKey(CalendarEntry, on_delete=models.CASCADE)

    class Meta:
        """Meta options for the Subscription model."""

        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self) -> str:
        """Return a string representation of the Subscription."""
        return f"{self.product.product.name} - {self.customer.name}"
