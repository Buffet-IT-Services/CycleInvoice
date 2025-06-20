"""Test cases for the Vehicle model."""

from django.test import TestCase

from cycle_invoice.common.selectors import get_object
from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.vehicle.models import Vehicle


def fake_vehicle(save: bool) -> Vehicle:  # noqa: FBT001
    """Create a fake work type."""
    vehicle = get_object(
        Vehicle,
        name_internal="Test Vehicle",
    )
    if vehicle is None:
        vehicle = Vehicle(
            name_internal="Test Vehicle",
            name_external="Test Vehicle External",
            km_buy=1.0,
            km_sell=2.0
        )
        if save:
            vehicle.save(user=get_default_test_user())
    return vehicle


class VehicleTest(TestCase):
    """Test cases for the WorkType model."""

    def test_str(self) -> None:
        """Test the string representation of the Vehicle model."""
        self.assertEqual("Test Vehicle", str(fake_vehicle(save=False)))
