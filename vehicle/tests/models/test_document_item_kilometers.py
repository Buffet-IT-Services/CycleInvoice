"""Test cases for the Vehicle model."""

from django.test import TestCase

from contact.tests.models.test_address import fake_address
from contact.tests.models.test_contact import fake_contact
from vehicle.models import DocumentItemKilometers
from vehicle.tests.models.test_vehicle import fake_vehicle


def fake_document_item_kilometers() -> DocumentItemKilometers:
    """Create a fake document item kilometers."""
    vehicle = fake_vehicle()
    address = fake_address()
    return DocumentItemKilometers.objects.create(
        vehicle=vehicle, start_address=address, end_address=address, price=100.0, quantity=1.0, customer=fake_contact()
    )


class VehicleTest(TestCase):
    """Test cases for the WorkType model."""

    def test_title_str(self) -> None:
        """Test the title property of the DocumentItemKilometers model."""
        self.assertEqual("Kilometer expense for Test Vehicle External", fake_document_item_kilometers().title_str)

    def test_comment_str(self) -> None:
        """Test the comment property of the DocumentItemKilometers model."""
        self.assertEqual("Any town - Any town", fake_document_item_kilometers().comment_str)
