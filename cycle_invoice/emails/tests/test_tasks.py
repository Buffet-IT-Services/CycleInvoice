"""Tests for emails tasks."""

from unittest.mock import patch

from django.test import TestCase

from cycle_invoice.emails.models import Email
from cycle_invoice.emails.tasks import _email_send_failure, email_send
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

    def test_email_send_fail_wrong_status(self) -> None:
        """Test the email send task."""
        email = EmailFactory.create(status=Email.Status.FAILED)
        with self.assertRaises(ValueError):
            email_send(email.uuid)

    def test__email_send_failure_calls_email_failed(self) -> None:
        """If the email exists, email_failed is called."""
        email = EmailFactory.create()
        with patch("cycle_invoice.emails.tasks.email_failed") as mock_failed:
            _email_send_failure(None, Exception("send error"), None, (email.uuid,), {}, None)
            mock_failed.assert_called_once()
            called_email = mock_failed.call_args[0][0]
            # Compare by UUID as ORM instances may differ
            self.assertEqual(called_email.uuid, email.uuid)

    def test__email_send_failure_missing_email_raises(self) -> None:
        """If the email is not found, ValueError is raised."""
        with self.assertRaises(ValueError):
            _email_send_failure(None, Exception("send error"), None, ("4398f182-3c41-480a-afc7-15387ce5511c",), {},
                                None)
