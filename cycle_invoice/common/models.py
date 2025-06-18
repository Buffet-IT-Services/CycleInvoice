"""Base models for the Cycle Invoice application."""
import uuid

from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    """Base model to inherit from for common fields."""

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        editable=False,
        related_name="%(class)s_created_by"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        editable=False,
        related_name="%(class)s_updated_by"
    )
    soft_deleted = models.BooleanField(
        default=False
    )
    history = HistoricalRecords(
        inherit=True
    )

    class Meta:
        """Meta options for BaseModel."""

        abstract = True

    def save(self, *args, **kwargs) -> None:
        """Override save method to set created_by and updated_by."""
        user = kwargs.pop("user", None)
        if not user:
            error_message = "You must provide a user to save the model."
            raise ValueError(error_message)
        if not self.pk:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)

class TestBaseModel(BaseModel):
    """Test model to verify BaseModel functionality."""

    name = models.CharField(
        max_length=255,
        verbose_name="Name",
        default="",
        blank=True,
    )

    class Meta:
        """Meta options for TestBaseModel."""

        verbose_name = "Test Base Model"
        verbose_name_plural = "Test Base Models"

    def __str__(self) -> str:
        """Return str representation of the TestBaseModel."""
        return self.name
