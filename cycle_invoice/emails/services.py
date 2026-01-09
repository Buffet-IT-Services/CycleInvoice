"""Services for emails app."""

from constance import config
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.utils import timezone

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.common.services import model_update
from cycle_invoice.emails.models import Email


@transaction.atomic
def email_failed(email: Email) -> Email:
    """Mark an email as failed."""
    if email.status != Email.Status.SENDING:
        error_message = f"Cannot fail non-sending emails. Current status is {email.status}"
        raise ValueError(error_message)

    email, _ = model_update(instance=email, fields=["status"], data={"status": Email.Status.FAILED},
                            user=get_system_user())
    return email


@transaction.atomic
def email_send(email: Email) -> Email:
    """Send an email."""
    if email.status != Email.Status.SENDING:
        error_message = f"Cannot send non-sending emails. Current status is {email.status}"
        raise ValueError(error_message)

    # Ensure that the recipient email address is present and non-empty
    recipient_email = getattr(getattr(email, "to", None), "email", None)
    if not recipient_email or not str(recipient_email).strip():
        error_message = "Cannot send email without a valid recipient email address."
        raise ValueError(error_message)

    msg = EmailMultiAlternatives(
        subject=email.subject,
        body=email.plain_text,
        from_email=config.COMPANY_EMAIL_SEND,
        to=[recipient_email],
        reply_to=[config.COMPANY_EMAIL_REPLY_TO],
        headers={
            "X-CycleInvoice-UUID": str(email.uuid),
        },
    )
    msg.attach_alternative(email.html, "text/html")

    msg.send()

    email, _ = model_update(
        instance=email,
        fields=["status", "sent_at"],
        data={"status": Email.Status.SENT,
              "sent_at": timezone.now()},
        user=get_system_user(),
    )
    return email
