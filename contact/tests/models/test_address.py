"""Test cases for the Address model."""

from django.test import TestCase

from contact.models import Address


def fake_address() -> Address:
    """Create a fake address."""
    return Address.objects.create(street="Main St", number="1", city="Anytown", zip_code="1234", country="Switzerland")


def fake_address_with_additional() -> Address:
    """Create a fake address with additional info."""
    return Address.objects.create(
        street="Main St",
        number="1",
        additional="c/o Company",
        city="Anytown",
        zip_code="1234",
        country="Switzerland",
    )


class AddressTest(TestCase):
    """Test cases for the Address model."""

    def test_str(self) -> None:
        """Test the __str__ of Address."""
        address = fake_address()
        self.assertEqual("Main St 1, c/o Company, 1234 Anytown, Switzerland", str(address))

        address = fake_address_with_additional()
        self.assertEqual("Main St 1, 1234 Anytown, Switzerland", str(address))
