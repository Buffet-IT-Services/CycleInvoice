"""Celery settings for the Cycle Invoice."""
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

CELERY_RESULT_BACKEND = "django-db"

CELERY_TIMEZONE = os.getenv("TIME_ZONE", "UTC")

CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_TIME_LIMIT = 300  # 5 minutes

CELERY_TASK_MAX_RETRIES = 3
