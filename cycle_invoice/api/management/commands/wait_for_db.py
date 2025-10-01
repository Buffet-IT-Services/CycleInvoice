"""Django management command to wait for database availability."""

import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options) -> None:
        """Wait until the database is available or timeout occurs."""
        self.stdout.write("Waiting for database...")
        db_conn = None
        max_attempts = 30
        attempt = 0

        while not db_conn and attempt < max_attempts:
            try:
                db_conn = connections["default"]
                db_conn.cursor()
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(attempt)
                attempt += 1
            else:
                self.stdout.write(self.style.SUCCESS("Database available!"))
                return

        if attempt >= max_attempts:
            error_message = "Could not connect to database after multiple attempts"
            self.stdout.write(self.style.ERROR("Database connection timed out"))
            raise OperationalError(error_message)
