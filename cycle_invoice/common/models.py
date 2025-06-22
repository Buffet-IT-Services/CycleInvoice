"""Base models for the Cycle Invoice application."""
import uuid
from urllib.request import Request

from django.contrib.auth.models import User
from django.db import models
from simple_history.admin import SimpleHistoryAdmin
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

    def delete(self, *args, **kwargs) -> None:
        """Override delete method to implement soft delete."""
        hard_delete = kwargs.pop("hard_delete", False)
        if hard_delete:
            super().delete()
            return

        user = kwargs.pop("user", None)
        if not user:
            error_message = "You must provide a user to save the model."
            raise ValueError(error_message)

        # TODO: use update_model instead of directly modifying the field
        # https://github.com/Buffet-IT-Services/CycleInvoice/issues/67
        # Issue URL: https://github.com/Buffet-IT-Services/CycleInvoice/issues/67
        self.soft_deleted = True
        self.save(user=user)


class BaseModelAdmin(SimpleHistoryAdmin):
    """Base admin class for models inheriting from BaseModel."""

    def save_model(self, request: Request, obj: BaseModel, form: object, change: bool) -> None:  # noqa: FBT001,ARG002
        """Override save_model to set the user."""
        obj.save(user=request.user)


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
