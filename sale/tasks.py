"""Tasks from the app sale that are run by Celery."""
import logging

from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task
def subscription_processing_to_document_items():
    """
    Iterates through all active subscriptions and processes those
    whose next_end_billed_date is in bill_days_before_end days or less in the future.
    """
    logging.info("Starting subscription processing task...")
    from datetime import date
    from sale.models import Subscription
    from sale.services.subscription import subscription_extension

    today = date.today()
    subs = Subscription.objects.filter(canceled_date__isnull=True)
    for sub in subs:
        next_end = sub.next_end_billed_date
        bill_days = sub.product.bill_days_before_end
        if next_end and (next_end - today).days <= bill_days:
            logging.info(f"Processing subscription {sub.id} for billing.")
            subscription_extension(sub.id)
    logging.info("Finished subscription processing task.")
