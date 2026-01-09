"""Tests for emails tasks."""

from django.test import TestCase

from cycle_invoice.emails.models import Email
from cycle_invoice.emails.tasks import email_send
from cycle_invoice.emails.tests.factories import EmailFactory


class EmailsTest(TestCase):
    """Test case for emails tasks."""

    def test_email_send_success(self) -> None:
        """Test the email send task."""

        email = EmailFactory.create()
        email_send(email.uuid)
        email.refresh_from_db()
        self.assertEqual(email.status, Email.Status.SENT)

    def test_email_send_fail(self) -> None:
        """Test the email send task."""
        with self.assertRaises(ValueError):
            email_send("4398f182-3c41-480a-afc7-15387ce5511c")