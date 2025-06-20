"""Models for the product app."""
from django.db import models

from cycle_invoice.accounting.models import get_default_buy_account, Account, get_default_sell_account
from cycle_invoice.common.models import BaseModel
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Product(BaseModel):
    """Model representing a sale product."""

    name = models.CharField(
        _("name"),
        max_length=255
    )
    description = models.TextField(
        _("description"),
        blank=True
    )
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
    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("price"),
        null=True,
        blank=True
    )

    class Meta:
        """Meta options for the Product model."""

        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        """Return a string representation of the SaleProduct."""
        return self.name

