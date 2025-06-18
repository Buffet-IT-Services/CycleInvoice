"""Test cases for the Vehicle model."""

from django.test import TestCase

from cycle_invoice.vehicle.models import Vehicle


def fake_vehicle() -> Vehicle:
    """Create a fake work type."""
    return Vehicle(
        name_internal="Test Vehicle",
        name_external="Test Vehicle External",
        km_buy=1.0,
        km_sell=2.0
    )


class VehicleTest(TestCase):
    """Test cases for the WorkType model."""

    def test_str(self) -> None:
        """Test the string representation of the Vehicle model."""
        self.assertEqual("Test Vehicle", str(fake_vehicle()))
