"""Base models for the Cycle Invoice application."""
from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from simple_history.models import HistoricalRecords

from cycle_invoice.common.selectors import get_system_user

if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    """Base model to inherit from for common fields."""

    class ActiveQuerySet(models.QuerySet):
        """Custom QuerySet to filter active and deleted records."""

        def active(self) -> models.QuerySet:
            """Return only active records."""
            return self.filter(soft_deleted=False)

        def deleted(self) -> models.QuerySet:
            """Return only deleted records."""
            return self.filter(soft_deleted=True)

    class ActiveManager(models.Manager.from_queryset(ActiveQuerySet)):
        """Custom Manager to return active records."""

        def get_queryset(self) -> models.QuerySet:
            """Return the active records."""
            return super().get_queryset().active()

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        editable=False,
        related_name="%(class)s_created_by"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        editable=False,
        related_name="%(class)s_updated_by"
    )
    soft_deleted = models.BooleanField(
        _("soft deleted"),
        default=False,
        db_index=True,
    )
    history = HistoricalRecords(
        inherit=True
    )

    objects = ActiveManager()
    objects_with_deleted = models.Manager()

    class Meta:
        """Meta options for BaseModel."""

        abstract = True

    def save(self, *args, **kwargs) -> None:
        """Override save method to set created_by and updated_by."""
        user = kwargs.pop("user", None)

        if self.pk:
            db_soft_deleted = (self.__class__.objects_with_deleted
                               .filter(pk=self.pk)
                               .values_list("soft_deleted", flat=True)
                               .first())
            if db_soft_deleted:
                error_message = "Cannot update a soft-deleted object."
                raise ValueError(error_message)

        if not self.pk:
            self.created_by = user

        self.updated_by = user
        self.updated_at = timezone.now()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        """Override delete method to implement soft delete."""
        hard_delete = kwargs.pop("hard_delete", False)
        if hard_delete:
            super().delete()
            return

        user = kwargs.pop("user", None)
        if not user:
            error_message = "You must provide a user to delete the model."
            raise ValueError(error_message)

        self.updated_by = user
        self.updated_at = timezone.now()
        self._history_user = user
        self.soft_deleted = True

        super().save(*args, **kwargs)

    def recover(self, user: User) -> None:
        """Recover a soft-deleted object."""
        if not self.soft_deleted:
            error_message = "Object is not soft-deleted."
            raise ValueError(error_message)

        self.updated_by = user
        self.updated_at = timezone.now()
        self._history_user = user
        self.soft_deleted = False

        super().save()


class BaseModelAdmin(SimpleHistoryAdmin):
    """Base admin class for models inheriting from BaseModel."""

    def save_model(self, request: HttpRequest, obj: BaseModel,
                   form: object, change: bool) -> None:  # noqa: ARG002, FBT001
        """Override save_model to set the user."""
        obj.save(user=request.user)

    def delete_model(self, request: HttpRequest, obj: BaseModel) -> None:
        """Override delete to pass the user for soft-delete."""
        obj.delete(user=request.user)

    list_filter = ("soft_deleted",)
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")

    @admin.action(description="Soft delete selected")
    def soft_delete_selected(self, request: HttpRequest, queryset: models.QuerySet) -> None:
        """Soft delete selected records."""
        for obj in queryset:
            obj.delete(user=request.user)

    actions = ["soft_delete_selected"]


class CustomUserManager(BaseModel.ActiveManager, BaseUserManager):
    """Custom user manager."""

    def _create_user(self, email: str, password: str | None = None, **extra_fields) -> User:
        """Create and save a new user with given details."""
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        system_user = get_system_user()
        user.save(using=self._db, user=system_user)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields) -> User:
        """Create and save a new user with given details."""
        extra_fields["is_superuser"] = False
        extra_fields["is_staff"] = False
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields) -> User:
        """Create and save a new superuser with given details."""
        extra_fields["is_superuser"] = True
        extra_fields["is_staff"] = True
        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username: str) -> User:
        """Override this method to normalize the email input."""
        email = self.normalize_email(username)
        return self.get(**{self.model.USERNAME_FIELD: email})


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    """Custom user model."""

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self) -> str:
        """Return string representation of the user."""
        return self.email
