"""Model for inheriting change logger functionality."""
from django.db import models
from simple_history.models import HistoricalRecords


# Create your models here.
class ChangeLoggerAll(models.Model):
    """Model representing a change logger."""

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
