"""Test cases for the Organisation model."""
from django.test import TestCase

from contact.models import Organisation


class OrganisationTest(TestCase):
    """Test cases for the Customer model."""

    def test_str(self) -> None:
        """Test the __str__ of organisation."""

        organisation = Organisation.objects.create(name="Test Org")
        self.assertEqual(str(organisation), "Test Org")