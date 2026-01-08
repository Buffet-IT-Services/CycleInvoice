"""Tests for sale management commands."""
from django.core.management import call_command
from django.test import TestCase
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class SetupPeriodicTasksCommandTest(TestCase):
    """Test case for setup_periodic_tasks management command."""

    def test_setup_periodic_tasks_creates_schedule_and_task(self) -> None:
        """Test that the command creates the crontab schedule and periodic task."""
        # Ensure no tasks exist initially
        self.assertEqual(PeriodicTask.objects.count(), 0)
        
        # Run the management command
        call_command("setup_periodic_tasks")
        
        # Verify the crontab schedule was created
        schedule = CrontabSchedule.objects.get(
            minute="0",
            hour="0",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        )
        self.assertIsNotNone(schedule)
        
        # Verify the periodic task was created
        task = PeriodicTask.objects.get(name="process-subscriptions-daily")
        self.assertEqual(task.task, "cycle_invoice.sale.tasks.subscription_processing_to_document_items")
        self.assertEqual(task.crontab, schedule)
        self.assertTrue(task.enabled)

    def test_setup_periodic_tasks_updates_existing_task(self) -> None:
        """Test that the command updates an existing periodic task."""
        # Create an existing task with different settings
        schedule = CrontabSchedule.objects.create(
            minute="0",
            hour="0",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        )
        task = PeriodicTask.objects.create(
            name="process-subscriptions-daily",
            task="old.task.path",
            crontab=schedule,
            enabled=False,
        )
        
        # Run the management command
        call_command("setup_periodic_tasks")
        
        # Verify the task was updated
        task.refresh_from_db()
        self.assertEqual(task.task, "cycle_invoice.sale.tasks.subscription_processing_to_document_items")
        self.assertTrue(task.enabled)

    def test_setup_periodic_tasks_is_idempotent(self) -> None:
        """Test that running the command multiple times doesn't create duplicates."""
        # Run the command twice
        call_command("setup_periodic_tasks")
        call_command("setup_periodic_tasks")
        
        # Verify only one task exists
        self.assertEqual(PeriodicTask.objects.filter(name="process-subscriptions-daily").count(), 1)
        
        # Verify only one schedule exists
        self.assertEqual(CrontabSchedule.objects.filter(
            minute="0",
            hour="0",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        ).count(), 1)
