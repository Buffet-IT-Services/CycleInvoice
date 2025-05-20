"""Test cases for the customer model."""

from django.test import TestCase

from contact.tests.models.test_address import fake_address, fake_address_with_additional
from contact.tests.models.test_contact import fake_contact


class ContactTest(TestCase):
    """Test cases for the customer model."""

    def test_prop_address_block(self) -> None:
        """Test the property address_block of customer."""
        contact = fake_contact()
        self.assertEqual("John Doe", contact.address_block)

        contact.address = fake_address()
        self.assertEqual("John Doe\nMain St 1\n1234 Any town\nSwitzerland", contact.address_block)

        contact.address = fake_address_with_additional()
        self.assertEqual("John Doe\nc/o Company\nMain St 1\n1234 Any town\nSwitzerland", contact.address_block)
