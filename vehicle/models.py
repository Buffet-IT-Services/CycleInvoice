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
