"""Tests for the party model Address."""

from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.party.tests.factories import AddressFactory


class TestModelAddress(TestCase):
    """Tests for the party model Address."""

    def setUp(self) -> None:
        """Set up the test environment."""

        self.user = get_system_user()
        self.address = AddressFactory.create()
        self.swiss_address = AddressFactory.create(country="CH")

    def test_address_str(self) -> None:
        """Test Address.__str__()."""

        self.assertEqual(str(self.address), self.address.address_line_1)
