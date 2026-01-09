"""Models for emails app."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from cycle_invoice.common.models import BaseModel


class Email(BaseModel):
    """Model representing an email."""

    class Status(models.TextChoices):
        """Status choices for the Email model."""

        READY = "READY", "Ready"
        SENDING = "SENDING", "Sending"
        SENT = "SENT", "Sent"
        FAILED = "FAILED", "Failed"

    status = models.CharField(max_length=255, db_index=True, choices=Status.choices, default=Status.READY)

    to = models.ForeignKey("party.Party",
                           on_delete=models.PROTECT,
                           related_name="sent_emails",
                           verbose_name=_("email to"))
    subject = models.CharField(max_length=255)

    html = models.TextField()
    plain_text = models.TextField()

    sent_at = models.DateTimeField(blank=True, null=True)
