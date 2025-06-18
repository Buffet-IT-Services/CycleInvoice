"""Test cases for selector of address."""
from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_user
from cycle_invoice.contact.selectors.address import address_get, address_list
from cycle_invoice.contact.tests.models.test_address import fake_address


class AddressTest(TestCase):
    """Test cases for selectors related to Address."""

    def setUp(self) -> None:
        """Set up test data for Address selectors."""
        self.user = get_default_user()
        self.address1 = fake_address()
        self.address1.save(user=self.user)
        self.address2 = fake_address()
        self.address2.save(user=self.user)

    def test_address_list_returns_all(self) -> None:
        """Test that address_list returns all addresses."""
        qs = address_list()
        self.assertIn(self.address1, qs)
        self.assertIn(self.address2, qs)
        self.assertEqual(qs.count(), 2)

    def test_address_get_returns_address(self) -> None:
        """Test that address_get returns the correct address."""
        address = address_get(self.address1.id)
        self.assertEqual(address, self.address1)

    def test_address_get_returns_none_for_invalid_id(self) -> None:
        """Test that address_get returns None for an invalid ID."""
        address = address_get(99999)
        self.assertIsNone(address)
