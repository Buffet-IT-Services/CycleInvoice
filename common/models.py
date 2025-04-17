"""Model for inheriting change logger functionality."""

from django.db import models
from simple_history.models import HistoricalRecords


class ChangeLoggerAll(models.Model):
    """Model representing a change logger."""

    history = HistoricalRecords(inherit=True)

    class Meta:
        """Meta options for the ChangeLoggerAll model."""

        abstract = True
