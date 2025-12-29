"""Celery settings for the Cycle Invoice."""
import os

from celery.schedules import crontab

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE", "UTC")

CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_TIME_LIMIT = 300  # 5 minutes

CELERY_BEAT_SCHEDULE = {
    "process-subscriptions-daily": {
        "task": "cycle_invoice.sale.tasks.subscription_processing_to_document_items",
        "description": "Creates billable items from subscriptions.",
        "schedule": crontab(hour=0, minute=0),
    },
}
