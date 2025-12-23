"""Models for the web application."""

from django.db import models

from cycle_invoice.common.models import BaseModel
from cycle_invoice.party.models import Party


class Domain(BaseModel):
    """Model representing a domain."""

    name = models.CharField(
        max_length=255,
        unique=True
    )
    party = models.ForeignKey(
        Party,
        on_delete=models.CASCADE
    )

    class Meta:
        """Meta options for the Domain model."""

        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    def __str__(self) -> str:
        """Return a string representation of the Domain."""
        return self.name
