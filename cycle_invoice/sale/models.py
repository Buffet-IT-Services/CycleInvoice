"""A module for sale models."""

from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from cycle_invoice.common.models import BaseModel, BasePolymorphicModel, DiscountType


class Document(BaseModel):
    """Model representing a document."""

    party = models.ForeignKey(
        "party.Party",
        on_delete=models.CASCADE,
        related_name="document_invoice"
    )
    document_number = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("document number")
    )
    date = models.DateField(
        verbose_name=_("date")
    )
    header_text = models.TextField(
        verbose_name=_("header text"),
        blank=True
    )
    footer_text = models.TextField(
        verbose_name=_("footer text"),
        blank=True
    )

    def __str__(self) -> str:
        """Return a string representation of the DocumentInvoice."""
        return f"{self.document_number} - {self.party}"


class Invoice(Document):
    """Model representing an invoice."""

    due_date = models.DateField(
        verbose_name=_("due date")
    )

    class Meta:
        """Meta-options for the Invoice model."""

        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    @property
    def total_sum(self) -> Decimal:
        """The sum of the totals of all DocumentItems belonging to this invoice."""
        return sum((item.total for item in self.document_item.all()), start=Decimal(0))


class DocumentItem(BasePolymorphicModel):
    """Model representing a document item."""

    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("price")
    )
    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("quantity")
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="document_item",
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("title"),
        blank=True,
        default=""
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True,
        default=""
    )
    party = models.ForeignKey(
        "party.Party",
        on_delete=models.CASCADE,
        related_name="sale_document_item_party",
    )
    account = models.ForeignKey(
        "accounting.Account",
        on_delete=models.PROTECT,
        related_name="sale_document_item_account",
    )
    discount_value = models.DecimalField(
        verbose_name=_("discount value"),
        max_digits=14,
        decimal_places=2,
        default=0
    )
    discount_type = models.CharField(
        verbose_name=_("discount type"),
        max_length=10,
        choices=DiscountType.choices,
        default=DiscountType.PERCENT,
    )

    @property
    def price_str(self) -> str:
        """Return the price as a string."""
        return f"{Decimal(str(self.price)):.2f}"

    @property
    def quantity_str(self) -> str:
        """Return the quantity as a string."""
        quantity = Decimal(str(self.quantity))
        if quantity == int(quantity):
            return str(int(quantity))
        return f"{quantity:.2f}".rstrip("0").rstrip(".")

    @property
    def total(self) -> Decimal:
        """Return the total price considering discount."""
        price = Decimal(str(self.price))
        quantity = Decimal(str(self.quantity))
        discount_value = Decimal(str(self.discount_value))

        if self.discount_type == DiscountType.ABSOLUTE:
            total = price * quantity - discount_value
        else:
            total = price * quantity * (Decimal(1) - discount_value / Decimal(100))
        return round(total, 2)

    @property
    def total_str(self) -> str:
        """Return the total price as a string."""
        return f"{self.total:.2f}"

    @property
    def discount_str(self) -> str:
        """Return the discount percentage as a string."""
        discount_value = Decimal(str(self.discount_value))
        if self.discount_type == DiscountType.ABSOLUTE:
            return f"-{discount_value:.2f}" if discount_value != 0 else ""
        return f"{(100 * discount_value):.2f}%" if discount_value != 0 else ""
