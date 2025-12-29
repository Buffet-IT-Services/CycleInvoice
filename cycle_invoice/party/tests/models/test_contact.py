"""Tests for the party model Contact."""
from django.db.models import ProtectedError
from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.party.tests.factories import ContactFactory


class TestContact(TestCase):
    """Tests for the party model Contact."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.user = get_system_user()
        self.contact = ContactFactory.create()
        self.contact_without_address = ContactFactory.build(address=None)

    def test_contact_str(self) -> None:
        """Test Organization.__str__()."""
        self.assertEqual(str(self.contact), f"{self.contact.first_name} {self.contact.last_name}")

    def test_contact_address_block(self) -> None:
        """Test Contact.address_block."""
        self.assertEqual(self.contact.address_block,
                         f"{self.contact.first_name} {self.contact.last_name}\n{self.contact.address.address_block}")

    def test_contact_address_block_without_address(self) -> None:
        """Test Contact.address_block."""
        self.assertEqual(self.contact_without_address.address_block,
                         f"{self.contact_without_address.first_name} {self.contact_without_address.last_name}")

    def test_contact_address_not_deletable(self) -> None:
        """Test Contact.address_block."""
        with self.assertRaises(ProtectedError):
            self.contact.address.delete(hard_delete=True)
