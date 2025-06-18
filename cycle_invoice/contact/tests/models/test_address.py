"""Test cases for the Address model."""

from django.test import TestCase

from cycle_invoice.contact.models import Address, address_block


def fake_address() -> Address:
    """Create a fake address."""
    return Address(
        street="Main St",
        number="1",
        city="Any town",
        zip_code="1234",
        country="Switzerland"
    )


def fake_address_with_additional() -> Address:
    """Create a fake address with additional info."""
    return Address(
        street="Main St",
        number="1",
        additional="c/o Company",
        city="Any town",
        zip_code="1234",
        country="Switzerland",
    )


class AddressTest(TestCase):
    """Test cases for the Address model."""

    def test_str(self) -> None:
        """Test the __str__ of Address."""
        address = fake_address_with_additional()
        self.assertEqual("c/o Company, Main St 1, 1234 Any town, Switzerland", str(address))

        address = fake_address()
        self.assertEqual("Main St 1, 1234 Any town, Switzerland", str(address))

    def test_address_block(self) -> None:
        """Test the address block function."""
        address = fake_address_with_additional()
        self.assertEqual("c/o Company\nMain St 1\n1234 Any town\nSwitzerland", address_block(address))

        address = fake_address()
        self.assertEqual("Main St 1\n1234 Any town\nSwitzerland", address_block(address))
