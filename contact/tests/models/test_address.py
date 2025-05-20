"""Test cases for the Address model."""

from django.test import TestCase

from contact.models import Address

def fake_address(with_additional: bool) -> Address:
    """Create a fake address."""
    if with_additional:
        return Address.objects.create(street="Main St", number="1", additional="c/o Company",
                                      city="Anytown", zip_code="1234", country="Switzerland")
    else:
        return Address.objects.create(street="Main St", number="1",
                                      city="Anytown", zip_code="1234", country="Switzerland")

class AddressTest(TestCase):
    """Test cases for the Address model."""

    def test_str(self) -> None:
        """Test the __str__ of Address."""
        address = fake_address(True)
        self.assertEqual("Main St 1, c/o Company, 1234 Anytown, Switzerland", str(address))

        address = fake_address(False)
        self.assertEqual("Main St 1, 1234 Anytown, Switzerland", str(address))
