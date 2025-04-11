"""A Sale Item model for representing work in a sale."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from contact.models import Contact, Organisation
from sale.models import SaleItem


class SaleWork(SaleItem):
    """Model representing a sale work item."""

    customer = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="sale_work_customer",
        verbose_name=_("customer"),
    )
    work_date = models.DateField(_("work date"))
    work_time = models.IntegerField(_("work time"), help_text=_("in minutes"))
    worker = models.ForeignKey(
        Contact,
        on_delete=models.PROTECT,
        related_name="sale_work_worker",
        verbose_name=_("worker"),
    )
    comment = models.TextField(_("comment"), max_length=255, blank=True)

    class Meta:
        """Meta options for the SaleWork model."""

        verbose_name = "Sale Work"
        verbose_name_plural = "Sale Works"

    def __str__(self) -> str:
        """Return a string representation of the sale work item."""
        return self.name
