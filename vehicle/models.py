"""Models for vehicle application."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import ChangeLoggerAll
from sale.models import DocumentItem


class Vehicle(ChangeLoggerAll):
    """Model representing a vehicle."""

    name_internal = models.CharField(_("internal name"), max_length=255, unique=True)
    name_external = models.CharField(_("external name"), max_length=50)
    km_buy = models.DecimalField(max_digits=14, decimal_places=2, verbose_name=_("km buy"), null=True, blank=True)
    km_sell = models.DecimalField(max_digits=14, decimal_places=2, verbose_name=_("km sell"), null=True, blank=True)

    class Meta:
        """Meta options for the Vehicle model."""

        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self) -> str:
        """Return the internal name of the vehicle."""
        return self.name_internal


class DocumentItemKilometers(DocumentItem):
    """Model representing a document item for kilometers."""

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="document_item_kilometers",
        verbose_name=_("vehicle"),
    )
    start_address = models.ForeignKey(
        "contact.Address",
        on_delete=models.PROTECT,
        related_name="document_item_kilometers_start_address",
        verbose_name=_("start address"),
    )
    end_address = models.ForeignKey(
        "contact.Address",
        on_delete=models.PROTECT,
        related_name="document_item_kilometers_end_address",
        verbose_name=_("end address"),
    )

    class Meta:
        """Meta options for the DocumentItemKilometers model."""

        verbose_name = "Document Kilometer"
        verbose_name_plural = "Document Kilometers"

    @property
    def title_str(self) -> str:
        """Return the work type name as the title."""
        return _("Kilometer expense for") + " " + self.vehicle.name_external

    @property
    def comment_str(self) -> str:
        """Return the work type description as the comment."""
        return self.start_address.city + " - " + self.end_address.city
