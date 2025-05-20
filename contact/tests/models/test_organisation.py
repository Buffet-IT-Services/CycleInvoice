"""Test cases for the Organisation model."""

from django.test import TestCase

from contact.models import Organisation


def fake_organisation() -> Organisation:
    """Create a fake organisation."""
    return Organisation.objects.create(name="Fake Org")


class OrganisationTest(TestCase):
    """Test cases for the Organisation model."""

    def test_str(self) -> None:
        """Test the __str__ of organisation."""
        organisation = fake_organisation()
        self.assertEqual(str(organisation), "Fake Org")
