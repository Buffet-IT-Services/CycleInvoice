"""Celery settings for the Cycle Invoice."""
import os

from celery.schedules import crontab

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", os.getenv("CELERY_BROKER_URL"))

CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE", "UTC")

CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_TIME_LIMIT = 300  # 5 minutes

# Use the database scheduler for better reliability in containerized environments
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Keep the schedule definition for initial setup and reference
# These will need to be added to the database via Django admin or management command
CELERY_BEAT_SCHEDULE = {
    "process-subscriptions-daily": {
        "task": "cycle_invoice.sale.tasks.subscription_processing_to_document_items",
        "schedule": crontab(hour=0, minute=0),
    },
}
