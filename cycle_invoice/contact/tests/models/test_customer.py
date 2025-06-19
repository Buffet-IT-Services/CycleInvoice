"""Test cases for the customer model."""

from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_user
from cycle_invoice.contact.models import Customer
from cycle_invoice.contact.tests.models.test_address import fake_address, fake_address_with_additional
from cycle_invoice.contact.tests.models.test_contact import fake_contact
from cycle_invoice.contact.tests.models.test_organisation import fake_organisation


class ContactTest(TestCase):
    """Test cases for the customer model."""

    def test_prop_address_block(self) -> None:
        """Test the property address_block of customer."""
        contact = fake_contact(save=False)
        self.assertEqual("John Doe", contact.address_block)

        contact.address = fake_address(save=False)
        self.assertEqual("John Doe\nMain St 1\n1234 Any town\nSwitzerland", contact.address_block)

        contact.address = fake_address_with_additional(save=False)
        self.assertEqual("John Doe\nc/o Company\nMain St 1\n1234 Any town\nSwitzerland", contact.address_block)

    def test__str__(self) -> None:
        """Test the __str__ method of customer."""
        contact = fake_contact(save=True)
        self.assertEqual("John Doe", Customer.__str__(contact))

        organization = fake_organisation(save=True)
        self.assertEqual("Fake Org", Customer.__str__(organization))

        self.assertEqual("Customer", Customer.__str__(Customer()))
