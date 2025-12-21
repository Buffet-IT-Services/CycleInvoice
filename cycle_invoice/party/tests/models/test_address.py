"""Tests for the party model Address."""

from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.party.tests.factories import AddressFactory


class TestAddress(TestCase):
    """Tests for the party model Address."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.user = get_system_user()
        self.address = AddressFactory.build(street="Musterstrasse", number="1", city="Musterstadt",
                                            zip_code="8000", country="Switzerland")
        self.address_with_additional = AddressFactory.build(street="Musterstrasse", number="1", city="Musterstadt",
                                                            zip_code="8000", country="Switzerland",
                                                            additional="c/o Max Muster")

    def test_address_str(self) -> None:
        """Test Address.__str__()."""
        self.assertEqual(str(self.address), "Musterstrasse 1, 8000 Musterstadt, Switzerland")

    def test_address_with_additional_str(self) -> None:
        """Test Address.__str__()."""
        self.assertEqual(str(self.address_with_additional),
                         "c/o Max Muster, Musterstrasse 1, 8000 Musterstadt, Switzerland")

    def test_address_block_default(self) -> None:
        """Test Address.block."""
        self.assertEqual(self.address.address_block, "Musterstrasse 1\n8000 Musterstadt\nSwitzerland")

    def test_address_with_additional_block(self) -> None:
        """Test Address.block."""
        self.assertEqual(self.address_with_additional.address_block,
                         "c/o Max Muster\nMusterstrasse 1\n8000 Musterstadt\nSwitzerland")
