"""Celery configuration for Cycle Invoice."""
from celery.schedules import crontab

CELERY_BROKER_URL = "redis://:foobared@redis:6379/0"

CELERY_TIMEZONE = "Europe/Zurich"

CELERY_TRACK_STARTED = True

CELERY_TASK_TIME_LIMIT = 300  # 5 minutes

CELERY_BEAT_SCHEDULE = {
    "process-subscriptions-daily": {
        "task": "sale.tasks.subscription_processing_to_document_items",
        "schedule": crontab(hour=0, minute=0),
    },
}