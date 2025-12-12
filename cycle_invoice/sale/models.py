"""A module for sale models."""

from decimal import Decimal

from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils.translation import gettext_lazy as _

from cycle_invoice.common.models import BaseModel


class Document(BaseModel):
    """Model representing a document."""

    party = models.ForeignKey(
        "contact.Party",
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


class Invoice(Document):
    """Model representing an invoice."""

    due_date = models.DateField(
        verbose_name=_("due date")
    )

    class Meta:
        """Meta options for the Invoice model."""

        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self) -> str:
        """Return a string representation of the DocumentInvoice."""
        return f"{self.invoice_number} - {self.customer}"

    @property
    def total_sum(self) -> Decimal:
        """The sum of the totals of all DocumentItems belonging to this invoice."""
        return sum((item.total for item in self.document_item.all()), start=Decimal(0))


class DocumentItem(BaseModel):
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
    discount = models.DecimalField(
        verbose_name=_("discount percent"),
        max_digits=5,
        decimal_places=4,
        default=0
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
        "contact.Party",
        on_delete=models.CASCADE,
        related_name="document_customer"
    )

    class DiscountType(models.TextChoices):
        """Discount types for document items."""
        PERCENT = "percent", "Percent"
        ABSOLUTE = "absolute", "Absolute"

    discount_type = models.CharField(
        max_length=50,
        choices=DiscountType.choices,
        verbose_name=_("discount type"),
        default=DiscountType.PERCENT,
    )

    @property
    def price_str(self) -> str:
        """Return the price as a string."""
        return f"{self.price:.2f}"

    @property
    def quantity_str(self) -> str:
        """Return the quantity as a string."""
        if self.quantity == int(self.quantity):
            return str(int(self.quantity))
        return f"{self.quantity:.2f}".rstrip("0").rstrip(".")

    @property
    def total(self) -> Decimal:
        """Return the total price."""
        return round(self.price * self.quantity * (1 - self.discount), 2)

    @property
    def total_str(self) -> str:
        """Return the total price as a string."""
        return f"{self.total:.2f}"

    @property
    def discount_str(self) -> str:
        """Return the discount percentage as a string."""
        return f"{(100 * self.discount):.2f}%" if self.discount != 0 else ""
