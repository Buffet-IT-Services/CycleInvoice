"""A module for sale models."""

from abc import abstractmethod
from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from recurring.models import CalendarEntry

from accounting.models import Account, get_default_buy_account, get_default_sell_account
from common.models import ChangeLoggerAll


class Product(ChangeLoggerAll):
    """Model representing a sale product."""

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
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
        return f"{self.product.name} - {self.get_recurrence_display()}"


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
        return f"{self.product.product.name} - {self.customer}"


class WorkType(ChangeLoggerAll):
    """Model representing a work type."""

    name = models.CharField(max_length=255, verbose_name=_("name"))
    account = models.ForeignKey(
        "accounting.Account",
        on_delete=models.SET_DEFAULT,
        default=get_default_sell_account,
        related_name="work_type_account",
    )

    class Meta:
        """Meta options for the WorkType model."""

        verbose_name = "Work Type"
        verbose_name_plural = "Work Types"

    def __str__(self) -> str:
        """Return a string representation of the WorkType."""
        return self.name


class WorkTypePrice(ChangeLoggerAll):
    """Model representing a work type price."""

    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, related_name="work_type_price")
    price = models.DecimalField(max_digits=14, decimal_places=2, verbose_name=_("price"))

    class Meta:
        """Meta options for the WorkTypePrice model."""

        verbose_name = "Work Type Price"
        verbose_name_plural = "Work Type Prices"

    def __str__(self) -> str:
        """Return a string representation of the WorkTypePrice."""
        return f"{self.work_type.name} - {self.price:.2f}"


class DocumentInvoice(ChangeLoggerAll):
    """Model representing a document invoice."""

    customer = models.ForeignKey("contact.Customer", on_delete=models.CASCADE, related_name="document_invoice")
    invoice_number = models.CharField(max_length=255, unique=True, verbose_name=_("invoice number"))
    date = models.DateField(verbose_name=_("date"))
    due_date = models.DateField(verbose_name=_("due date"))
    header_text = models.TextField(verbose_name=_("header text"), blank=True)
    footer_text = models.TextField(verbose_name=_("footer text"), blank=True)

    class Meta:
        """Meta options for the DocumentInvoice model."""

        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self) -> str:
        """Return a string representation of the DocumentInvoice."""
        return f"{self.invoice_number} - {self.customer}"


class DocumentItem(ChangeLoggerAll):
    """Model representing a document item."""

    price = models.DecimalField(max_digits=14, decimal_places=2, verbose_name=_("price"))
    quantity = models.DecimalField(max_digits=14, decimal_places=2, verbose_name=_("quantity"))
    discount = models.DecimalField(verbose_name=_("discount percent"), max_digits=5, decimal_places=4, default=0)
    item_group = models.CharField(max_length=255, verbose_name=_("item group"))
    invoice = models.ForeignKey(DocumentInvoice, on_delete=models.CASCADE, related_name="document_item", null=True)

    @property
    @abstractmethod
    def title_str(self) -> str:
        """Each child must implement a `title` property."""

    @property
    @abstractmethod
    def comment_str(self) -> str:
        """Each child must implement a `comment` property."""

    @property
    def price_str(self) -> str:
        """Return the price as a string."""
        return f"{self.price:.2f}"

    @property
    def quantity_str(self) -> str:
        """Return the quantity as a string."""
        return f"{self.quantity}"

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


class DocumentItemProduct(DocumentItem):
    """Model representing a document product."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="document_product")

    class Meta:
        """Meta options for the DocumentProduct model."""

        verbose_name = "Document Product"
        verbose_name_plural = "Document Products"

    @property
    def title_str(self) -> str:
        """Return the product name as the title."""
        return self.product.name

    @property
    def comment_str(self) -> str:
        """Return the product description as the comment."""
        return self.product.description if hasattr(self.product, "description") else ""


class DocumentItemWork(DocumentItem):
    """Model representing a document work."""

    comment = models.TextField(verbose_name=_("description"), blank=True)
    work = models.ForeignKey(WorkTypePrice, on_delete=models.CASCADE, related_name="document_work")

    class Meta:
        """Meta options for the DocumentWork model."""

        verbose_name = "Document Work"
        verbose_name_plural = "Document Works"

    @property
    def title_str(self) -> str:
        """Return the work type name as the title."""
        return self.work.work_type.name

    @property
    def comment_str(self) -> str:
        """Return the work type description as the comment."""
        return self.comment if self.comment else ""
