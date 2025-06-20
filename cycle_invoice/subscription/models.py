"""Models for the subscriptions app."""
from datetime import date

from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils.translation import gettext_lazy as _

from cycle_invoice.common.models import BaseModel
from cycle_invoice.product.models import Product


class SubscriptionProduct(BaseModel):
    """Model representing a subscription."""

    RECURRENCE_CHOICES = [
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="subscriptionproduct"
    )
    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("price")
    )
    recurrence = models.CharField(
        max_length=10,
        choices=RECURRENCE_CHOICES,
        default="yearly",
    )
    bill_days_before_end = models.PositiveIntegerField(
        verbose_name=_("bill x days before expiration"),
        default=20
    )

    class Meta:
        """Meta options for the Subscription model."""

        verbose_name = "Subscription Product"
        verbose_name_plural = "Subscription Products"

    def __str__(self) -> str:
        """Return a string representation of the Subscription."""
        return f"{self.product.name} - {self.get_recurrence_display()}"


class Subscription(BaseModel):
    """Model representing a subscription."""

    product = models.ForeignKey(
        SubscriptionProduct,
        on_delete=models.CASCADE,
        related_name="subscription"
    )
    customer = models.ForeignKey(
        "contact.Customer",
        on_delete=models.CASCADE,
        related_name="subscription"
    )
    start_date = models.DateField(
        verbose_name=_("start date")
    )
    end_billed_date = models.DateField(
        verbose_name=_("end billed date"),
        null=True,
        blank=True
    )
    cancelled_date = models.DateField(
        verbose_name=_("canceled date"),
        null=True,
        blank=True
    )

    class Meta:
        """Meta options for the Subscription model."""

        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self) -> str:
        """Return a string representation of the Subscription."""
        return f"{self.product.product.name} - {self.customer}"

    @property
    def is_cancelled(self) -> bool:
        """Check if the subscription is extending."""
        return self.cancelled_date is not None

    @property
    def next_start_billed_date(self) -> date:
        """Calculates the next billing date based on start_date and recurrence. Always returns a date object."""
        if not self.end_billed_date:
            return self.start_date
        return self.end_billed_date + relativedelta(days=+1)

    @property
    def next_end_billed_date(self) -> date:
        """Calculates the next billing date based on end_billed_date and recurrence."""
        if not self.end_billed_date:
            self.end_billed_date = self.start_date - relativedelta(days=1)
        recurrence = self.product.recurrence
        if recurrence == "monthly":
            return self.end_billed_date + relativedelta(days=1) + relativedelta(months=1) - relativedelta(days=1)
        if recurrence == "yearly":
            return self.end_billed_date + relativedelta(years=1)
        error_message = f"Recurrence type '{recurrence}' is unknown."
        raise ValueError(error_message)
