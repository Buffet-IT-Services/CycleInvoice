"""Tasks for emails app."""
from typing import Any
from uuid import UUID

from billiard.einfo import ExceptionInfo
from celery import shared_task
from celery.app.task import Task
from celery.utils.log import get_task_logger

from cycle_invoice.common.selectors import get_object
from cycle_invoice.emails.models import Email
from cycle_invoice.emails.services import email_failed

logger = get_task_logger(__name__)


def _email_send_failure(  # noqa: PLR0913
        task: Task,  # noqa:  ARG001
        exc: Exception,
        task_id: str | None,  # noqa:  ARG001
        args: tuple[Any, ...],
        kwargs: dict[str, Any],  # noqa:  ARG001
        einfo: ExceptionInfo,  # noqa:  ARG001
) -> None:
    """Handle an email send failure."""
    email_uuid: UUID = args[0]
    logger.warning("Email %s send failed: %s", email_uuid, exc)
    email = get_object(Email, uuid=email_uuid)
    if email is None:
        raise ValueError(f"Email with UUID {email_uuid} not found.")
    email_failed(email)


@shared_task(bind=True, on_failure=_email_send_failure)
def email_send(self: Task, email_uuid: UUID) -> None:
    """Send an email task using Celery."""
    email = get_object(Email, uuid=email_uuid)
    if email is None:
        raise ValueError(f"Email with UUID {email_uuid} not found.")

    from cycle_invoice.emails.services import email_send  # noqa: PLC0415

    try:
        email_send(email)
    except ValueError as exc:
        # https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
        logger.warning("Exception occurred while sending email: %s", exc)
        self.retry(exc=exc, countdown=5)
