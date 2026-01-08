"""Management command to set up periodic tasks in django-celery-beat."""
import logging

from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Set up periodic tasks for Celery Beat using django-celery-beat."""

    help = "Set up periodic tasks in the database for Celery Beat"

    def handle(self, *args, **options) -> None:
        """Create or update periodic tasks in the database."""
        self.stdout.write("Setting up periodic tasks...")

        # Create the crontab schedule (daily at midnight)
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour="0",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Created crontab schedule: daily at midnight"))
        else:
            self.stdout.write("Crontab schedule already exists")

        # Create or update the periodic task
        task, created = PeriodicTask.objects.get_or_create(
            name="process-subscriptions-daily",
            defaults={
                "task": "cycle_invoice.sale.tasks.subscription_processing_to_document_items",
                "crontab": schedule,
                "enabled": True,
            },
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('Created periodic task: "process-subscriptions-daily"')
            )
        else:
            # Update the task if it already exists
            task.task = "cycle_invoice.sale.tasks.subscription_processing_to_document_items"
            task.crontab = schedule
            task.enabled = True
            task.save()
            self.stdout.write(
                self.style.SUCCESS('Updated periodic task: "process-subscriptions-daily"')
            )

        self.stdout.write(self.style.SUCCESS("Periodic tasks setup complete!"))
