"""Test cases for the Organisation model."""

from django.test import TestCase

from cycle_invoice.contact.models import Organisation


def fake_organisation() -> Organisation:
    """Create a fake organisation."""
    return Organisation.objects.create(name="Fake Org")

def fake_organisation_with_name(name: str) -> Organisation:
    """Create a fake organisation with custom name."""
    return Organisation.objects.create(name=name)


class OrganisationTest(TestCase):
    """Test cases for the Organisation model."""

    def test_str(self) -> None:
        """Test the __str__ of organisation."""
        organisation = fake_organisation()
        self.assertEqual(str(organisation), "Fake Org")
