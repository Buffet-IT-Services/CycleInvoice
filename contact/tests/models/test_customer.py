"""Test cases for the customer model."""

from django.test import TestCase

from contact.models import Customer
from contact.tests.models.test_address import fake_address, fake_address_with_additional
from contact.tests.models.test_contact import fake_contact
from contact.tests.models.test_organisation import fake_organisation


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

    def test__str__(self) -> None:
        """Test the __str__ method of customer."""
        contact = fake_contact()
        self.assertEqual("John Doe", Customer.__str__(contact))

        organization = fake_organisation()
        self.assertEqual("Fake Org", Customer.__str__(organization))
