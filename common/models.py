"""Provides the base model for a tracked class."""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class TrackedBaseModel(models.Model):
    """
    Abstract base model for a tracked class.

    Tracks when the object was created and updated and by whom
    Tracks the history of the object
    """

    created_at = models.DateTimeField(verbose_name=_("Created at"), db_index=True, default=timezone.now)
    created_by = models.ForeignKey(get_user_model(), verbose_name=_("Created by"), on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)
    updated_by = models.ForeignKey(get_user_model(), verbose_name=_("Created by"), on_delete=models.SET_NULL, null=True)
    history = HistoricalRecords()

    class Meta:
        """Meta options for the TrackedBaseModel."""

        abstract = True
