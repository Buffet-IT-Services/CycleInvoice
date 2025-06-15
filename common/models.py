"""Model for inheriting change logger functionality."""

from django.db import models
from django.db.models import Q, F
from simple_history.models import HistoricalRecords


class ChangeLoggerAll(models.Model):
    """Model representing a change logger."""

    history = HistoricalRecords(inherit=True)

    class Meta:
        """Meta options for the ChangeLoggerAll model."""

        abstract = True


class BaseModel(models.Model):
    """Base model to inherit from for common fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the BaseModel."""
        abstract = True


class SimpleModel(models.Model):
    """
    This is a basic model used to illustrate a many-to-many relationship
    with RandomModel.
    """

    name = models.CharField(max_length=255, blank=True, null=True)


class RandomModel(BaseModel):
    """
    This is an example model, to be used as reference in the Styleguide,
    when discussing model validation via constraints.
    """

    start_date = models.DateField()
    end_date = models.DateField()

    simple_objects = models.ManyToManyField(
        SimpleModel, blank=True, related_name="random_objects"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="start_date_before_end_date", check=Q(start_date__lt=F("end_date"))
            )
        ]
