"""Test cases for the email_send method."""

from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.emails.models import Email
from cycle_invoice.emails.services import email_send
from cycle_invoice.emails.tests.factories import EmailFactory
from cycle_invoice.party.tests.factories import OrganizationFactory


class EmailSendTest(TestCase):
    """Test cases for the email_send method."""

    def test_email_send_wrong_status(self) -> None:
        """Test email_send() with a wrong status."""
        for status in Email.Status:
            if status != Email.Status.SENDING:
                email = EmailFactory.build(status=status)
                with self.assertRaises(ValueError):
                    email_send(email)

    def test_email_send_success(self) -> None:
        """Test email_send() with a correct status."""
        email = EmailFactory.create()
        email_send(email)
        self.assertEqual(email.status, Email.Status.SENT)
        self.assertIsNotNone(email.sent_at)
        self.assertEqual(email.updated_by, get_system_user())

    def test_email_send_no_mail(self) -> None:
        """Test email_send() with a non-existing email."""
        organization = OrganizationFactory.build(email="")
        email = EmailFactory.build(to=organization)
        with self.assertRaises(ValueError):
            email_send(email)
