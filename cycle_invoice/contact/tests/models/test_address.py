"""Test cases for the Address model."""

from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.contact.models import Address, address_block


def fake_address(
        save: bool,  # noqa: FBT001
) -> Address:
    """Create a fake address."""
    address = Address(
        street="Main St",
        number="1",
        city="Any town",
        zip_code="1234",
        country="Switzerland"
    )
    if save:
        address.save(user=get_default_test_user())
    return address


def fake_address_with_additional(
        save: bool,  # noqa: FBT001
) -> Address:
    """Create a fake address with additional info."""
    address = Address(
        street="Main St",
        number="1",
        additional="c/o Company",
        city="Any town",
        zip_code="1234",
        country="Switzerland",
    )
    if save:
        address.save(user=get_default_test_user())
    return address


class AddressTest(TestCase):
    """Test cases for the Address model."""

    def test_str(self) -> None:
        """Test the __str__ of Address."""
        address = fake_address_with_additional(save=False)
        self.assertEqual("c/o Company, Main St 1, 1234 Any town, Switzerland", str(address))

        address = fake_address(save=False)
        self.assertEqual("Main St 1, 1234 Any town, Switzerland", str(address))

    def test_address_block(self) -> None:
        """Test the address block function."""
        address = fake_address_with_additional(save=False)
        self.assertEqual("c/o Company\nMain St 1\n1234 Any town\nSwitzerland", address_block(address))

        address = fake_address(save=False)
        self.assertEqual("Main St 1\n1234 Any town\nSwitzerland", address_block(address))
