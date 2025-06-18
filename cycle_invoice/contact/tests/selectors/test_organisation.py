"""Test cases for the Organisation selector."""
from django.test import TestCase

from cycle_invoice.contact.selectors.organisation import organisation_get, organisation_list
from cycle_invoice.contact.tests.models.test_organisation import fake_organisation, fake_organisation_with_name


class OrganisationTest(TestCase):
    """Test cases for selectors regarding Organisation."""

    def setUp(self) -> None:
        """Set up test data for Organisation selectors."""
        self.organisation1 = fake_organisation()
        self.organisation2 = fake_organisation_with_name("Test Organisation")

    def test_organisation_list_returns_all(self) -> None:
        """Test that organisation_list returns all organisations."""
        qs = organisation_list()
        self.assertIn(self.organisation1, qs)
        self.assertIn(self.organisation2, qs)
        self.assertEqual(qs.count(), 2)

    def test_organisation_get_returns_organisation(self) -> None:
        """Test that organisation_get returns the correct organisation."""
        organisation = organisation_get(self.organisation1.id)
        self.assertEqual(organisation, self.organisation1)

    def test_organisation_get_returns_none_for_invalid_id(self) -> None:
        """Test that organisation_get returns None for an invalid ID."""
        organisation = organisation_get(99999)
        self.assertIsNone(organisation)
