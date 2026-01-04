"""Tests for the method createsuperuserifnew."""
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from cycle_invoice.common.models import User


class TestCreateSuperuserIfNew(TestCase):
    """Tests for the management command `createsuperuserifnew`."""

    def test_creates_superuser_when_missing(self) -> None:
        """Command should create a superuser when one does not exist for the email."""
        email = "admin@example.com"
        password = "password"

        self.assertFalse(User.objects.filter(email=email).exists())

        out = StringIO()
        call_command("createsuperuserifnew", "--email", email, "--password", password, stdout=out)

        output = out.getvalue()
        self.assertIn("Superuser created successfully", output)

        user = User.objects.get(email=email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_warns_when_user_exists(self) -> None:
        """Command should warn and not create a duplicate when the email already exists."""
        email = "existing@example.com"
        password = "password"

        User.objects.create_superuser(email=email, password=password)

        out = StringIO()
        call_command("createsuperuserifnew", "--email", email, "--password", "ignored", stdout=out)

        output = out.getvalue()
        self.assertIn("Superuser already exists", output)

        self.assertEqual(User.objects.filter(email=email).count(), 1)
