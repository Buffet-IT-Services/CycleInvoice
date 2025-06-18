"""Model for inheriting change logger functionality."""
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Q
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    """Base model to inherit from for common fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, related_name="%(class)s_created_by")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="%(class)s_updated_by")
    soft_deleted = models.BooleanField(default=False)
    history = HistoricalRecords(inherit=True)

    class Meta:
        """Meta options for the BaseModel."""

        abstract = True


class SimpleModel(models.Model):
    """Basic model used to illustrate a many-to-many relationship with RandomModel."""

    name = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        """Return a string representation of the SimpleModel."""
        return self.name or "Unnamed SimpleModel"


class RandomModel(BaseModel):
    """Basic model with a date range and a many-to-many relationship with SimpleModel."""

    start_date = models.DateField()
    end_date = models.DateField()

    simple_objects = models.ManyToManyField(
        SimpleModel, blank=True, related_name="random_objects"
    )

    class Meta:
        """Meta options for the RandomModel."""

        constraints = [
            models.CheckConstraint(
                name="start_date_before_end_date", check=Q(start_date__lt=F("end_date"))
            )
        ]

    def __str__(self) -> str:
        """Return a string representation of the RandomModel."""
        return f"RandomModel from {self.start_date} to {self.end_date}"
