"""Test cases for the Contact model."""

from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.contact.models import Contact


def fake_contact(
        save: bool  # noqa: FBT001
) -> Contact:
    """Create a fake contact."""
    contact = Contact(
        first_name="John",
        last_name="Doe"
    )
    if save:
        contact.save(user=get_default_test_user())
    return contact


class ContactTest(TestCase):
    """Test cases for the customer model."""

    def test_str(self) -> None:
        """Test the __str__ of Contact."""
        self.assertEqual(str(fake_contact(save=False)), "John Doe")
