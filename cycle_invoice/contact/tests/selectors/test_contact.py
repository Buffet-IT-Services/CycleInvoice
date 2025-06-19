"""Test cases for the Contact selector."""
from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_user
from cycle_invoice.contact.selectors.contact import contact_get, contact_list
from cycle_invoice.contact.tests.models.test_contact import fake_contact


class ContactTest(TestCase):
    """Test cases for selectors regarding Contact."""

    def setUp(self) -> None:
        """Set up test data for Contact selectors."""
        self.user = get_default_user()
        self.contact1 = fake_contact(save=True)
        self.contact2 = fake_contact(save=True)

    def test_contact_list_returns_all(self) -> None:
        """Test that contact_list returns all contacts."""
        qs = contact_list()
        self.assertIn(self.contact1, qs)
        self.assertIn(self.contact2, qs)
        self.assertEqual(qs.count(), 2)

    def test_contact_get_returns_contact(self) -> None:
        """Test that contact_get returns the correct contact."""
        contact = contact_get(self.contact1.id)
        self.assertEqual(contact, self.contact1)

    def test_contact_get_returns_none_for_invalid_id(self) -> None:
        """Test that contact_get returns None for an invalid ID."""
        contact = contact_get(99999)
        self.assertIsNone(contact)
