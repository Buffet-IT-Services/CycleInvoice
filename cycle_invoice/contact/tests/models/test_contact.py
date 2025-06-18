"""Test cases for the Contact model."""

from django.test import TestCase

from cycle_invoice.contact.models import Contact


def fake_contact() -> Contact:
    """Create a fake contact."""
    return Contact(
        first_name="John",
        last_name="Doe"
    )


class ContactTest(TestCase):
    """Test cases for the customer model."""

    def test_str(self) -> None:
        """Test the __str__ of Contact."""
        contact = fake_contact()
        self.assertEqual(str(contact), "John Doe")
