"""Test cases for a selector of Contact."""
from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.party.selectors.contact import contact_get, contact_list
from cycle_invoice.party.tests.factories import ContactFactory


class ContactTest(TestCase):
    """Test cases for selectors related to Contact."""

    def setUp(self) -> None:
        """Set up test data for Address selectors."""
        self.user = get_system_user()
        self.contact1 = ContactFactory.create()
        self.contact2 = ContactFactory.create(soft_deleted=True)

    def test_contact_list_returns_active(self) -> None:
        """Test that contact_list returns all addresses."""
        qs = contact_list()
        self.assertIn(self.contact1, qs)
        self.assertNotIn(self.contact2, qs)

    def test_contact_get_returns_uuid(self) -> None:
        """Test that contact_list returns the correct contact."""
        contact = contact_get(self.contact1.uuid)
        self.assertEqual(contact, self.contact1)

    def test_contact_get_returns_id(self) -> None:
        """Test that contact_list returns the correct contact."""
        contact = contact_get(self.contact1.id)
        self.assertEqual(contact, self.contact1)

    def test_contact_get_returns_none_for_invalid_id(self) -> None:
        """Test that contact_list returns None for an invalid ID."""
        contact = contact_get(99999)
        self.assertIsNone(contact)
