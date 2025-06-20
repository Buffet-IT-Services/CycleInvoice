"""Tasks from the app sale that are run by Celery."""
import datetime
import logging

from celery import shared_task

from cycle_invoice.common.system import get_system_user
from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.sale.models import Subscription
from cycle_invoice.sale.services.subscription import subscription_extension

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
    subs = Subscription.objects.filter(cancelled_date__isnull=True)
    for sub in subs:
        next_end = sub.end_billed_date
        bill_days = sub.product.bill_days_before_end
        if next_end and (next_end - today).days <= bill_days:
            log_message = f"Processing subscription {sub.id} with end_billed_date {next_end}"
            logger.info(log_message)
            subscription_extension(sub.id, user=get_system_user())
    logger.info("Finished subscription processing task.")
