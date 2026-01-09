"""Setup periodic tasks command."""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import get_default_timezone_name
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    """Setup periodic tasks command."""

    help = """
    Setup celery beat periodic tasks.

    Following tasks will be created:

        - Process subscriptions daily at 00:00
    """

    @transaction.atomic
    def handle(self, *args, **kwargs) -> None:
        """Handle command."""

        print("Deleting all periodic tasks and schedules...\n")

        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        periodic_tasks_data = [
            {
                "task": "cycle_invoice.sale.tasks.subscription_processing_to_document_items",
                "name": "Process subscriptions daily",
                "cron": {
                    "minute": "0",
                    "hour": "0",
                    "day_of_week": "*",
                    "day_of_month": "*",
                    "month_of_year": "*",
                },
                "enabled": True,
            },
        ]

        timezone = get_default_timezone_name()

        for periodic_task in periodic_tasks_data:
            print(f'Setting up {periodic_task["task"].name}')

            cron = CrontabSchedule.objects.create(timezone=timezone, **periodic_task["cron"])

            PeriodicTask.objects.create(
                name=periodic_task["name"],
                task=periodic_task["task"].name,
                crontab=cron,
                enabled=periodic_task["enabled"],
            )
