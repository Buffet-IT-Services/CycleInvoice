"""Command to create a superuser if it does not exist yet."""
from django.core.management import CommandParser
from django.core.management.base import BaseCommand

from cycle_invoice.common.models import User


class Command(BaseCommand):
    """Command to create a superuser if it does not exist yet."""

    help = "Create a superuser with predefined credentials"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add custom arguments to the command."""
        parser.add_argument("--email", type=str, required=True, help="Email for the superuser")
        parser.add_argument("--password", type=str, required=True, help="Password for the superuser")

    def handle(self, *args, **options) -> None:
        """Create a superuser if it does not exist yet."""
        email = options["email"]
        password = options["password"]

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING("Superuser already exists"))
        else:
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
