"""Tasks from the app sale that Celery runs."""
import datetime
import logging

from celery import shared_task

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.subscription.models import Subscription
from cycle_invoice.subscription.services.subscription import subscription_extension

logger = logging.getLogger(__name__)

@shared_task
def subscription_processing_to_document_items() -> None:
    """
    Process subscriptions for billing.

    Iterates through all active subscriptions and processes those
    whose next_end_billed_date is in bill_days_before_end days or less in the future.
    """
    logger.info("Starting subscription processing task...")

    today = datetime.datetime.now(tz=datetime.UTC).date()
    system_user = get_system_user()
    subscriptions = Subscription.objects.filter(cancelled_date__isnull=True).select_related(
        "plan",
        "plan__product",
        "plan__product__account_sell",
        "party",
    )
    for sub in subscriptions:
        next_end = sub.end_billed_date
        bill_days = sub.plan.bill_days_before_end
        if next_end and (next_end - today).days <= bill_days:
            log_message = f"Processing subscription {sub.id} with end_billed_date {next_end}"
            logger.info(log_message)
            subscription_extension(sub, user=system_user)
    logger.info("Finished subscription processing task.")
