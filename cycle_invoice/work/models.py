"""Models for the work app."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from cycle_invoice.accounting.models import get_default_sell_account
from cycle_invoice.common.models import BaseModel


class WorkType(BaseModel):
    """Model representing a work type."""

    name = models.CharField(
        max_length=255,
        verbose_name=_("name")
    )
    account = models.ForeignKey(
        "accounting.Account",
        on_delete=models.SET_DEFAULT,
        default=get_default_sell_account,
        related_name="work_type_account",
    )
    price_per_hour = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("price per hour")
    )

    class Meta:
        """Meta options for the WorkType model."""

        verbose_name = "Work Type"
        verbose_name_plural = "Work Types"

    def __str__(self) -> str:
        """Return a string representation of the WorkType."""
        return f"{self.name} - {self.price_per_hour:.2f}"
