"""Test cases for the email_failed method."""

from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.emails.models import Email
from cycle_invoice.emails.services import email_failed
from cycle_invoice.emails.tests.factories import EmailFactory


class EmailFailedTest(TestCase):
    """Test cases for the email_failed method."""

    def test_email_failed_wrong_status(self) -> None:
        """Test email_failed() with a wrong status."""

        for status in Email.Status:
            if status != Email.Status.SENDING:
                email = EmailFactory.build(status=status)
                with self.assertRaises(ValueError):
                    email_failed(email)

    def test_email_failed_success(self) -> None:
        """Test email_failed() with a correct status."""
        email = EmailFactory.create()
        email_failed(email)
        self.assertEqual(email.status, Email.Status.FAILED)
        self.assertIsNone(email.sent_at)
        self.assertEqual(email.updated_by, get_system_user())
