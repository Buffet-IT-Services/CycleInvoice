"""Test cases for a selector of Organization."""
from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.party.selectors.organization import organization_get, organization_list
from cycle_invoice.party.tests.factories import OrganizationFactory


class OrganizationTest(TestCase):
    """Test cases for selectors related to Organization."""

    def setUp(self) -> None:
        """Set up test data for Organization selectors."""
        self.user = get_system_user()
        self.organization1 = OrganizationFactory.create()
        self.organization2 = OrganizationFactory.create(soft_deleted=True)

    def test_organization_list_returns_active(self) -> None:
        """Test that organization_list returns all organizations."""
        qs = organization_list()
        self.assertIn(self.organization1, qs)
        self.assertNotIn(self.organization2, qs)

    def test_organization_get_returns_uuid(self) -> None:
        """Test that organization_get returns the correct organization."""
        organization = organization_get(self.organization1.uuid)
        self.assertEqual(organization, self.organization1)

    def test_organization_get_returns_none_for_invalid_id(self) -> None:
        """Test that organization_get returns None for an invalid ID."""
        organization = organization_get("99999")
        self.assertIsNone(organization)
