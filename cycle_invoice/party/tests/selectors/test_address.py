"""Test cases for a selector of address."""
from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.party.selectors.address import address_get, address_list
from cycle_invoice.party.tests.factories import AddressFactory


class AddressTest(TestCase):
    """Test cases for selectors related to Address."""

    def setUp(self) -> None:
        """Set up test data for Address selectors."""
        self.user = get_system_user()
        self.address1 = AddressFactory.create()
        self.address2 = AddressFactory.create(soft_deleted=True)

    def test_address_list_returns_active(self) -> None:
        """Test that address_list returns all addresses."""
        qs = address_list()
        self.assertIn(self.address1, qs)
        self.assertNotIn(self.address2, qs)

    def test_address_get_returns_address_uuid(self) -> None:
        """Test that address_get returns the correct address."""
        address = address_get(self.address1.uuid)
        self.assertEqual(address, self.address1)

    def test_address_get_returns_address_id(self) -> None:
        """Test that address_get returns the correct address."""
        address = address_get(self.address1.id)
        self.assertEqual(address, self.address1)

    def test_address_get_returns_none_for_invalid_id(self) -> None:
        """Test that address_get returns None for an invalid ID."""
        address = address_get(99999)
        self.assertIsNone(address)
