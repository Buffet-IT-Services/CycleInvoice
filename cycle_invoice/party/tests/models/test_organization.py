"""Tests for the party model Organization."""
from django.db.models import ProtectedError
from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.party.tests.factories import OrganizationFactory


class TestOrganization(TestCase):
    """Tests for the party model Organization."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.user = get_system_user()
        self.organization = OrganizationFactory.create()
        self.organization_without_address = OrganizationFactory.build(address=None)

    def test_organization_str(self) -> None:
        """Test Organization.__str__()."""
        self.assertEqual(str(self.organization), self.organization.name)

    def test_organization_address_block(self) -> None:
        """Test Organization.address_block."""
        self.assertEqual(self.organization.address_block,
                         f"{self.organization.name}\n{self.organization.address.address_block}")

    def test_contact_address_block_without_address(self) -> None:
        """Test Contact.address_block."""
        self.assertEqual(self.organization_without_address.address_block,
                         f"{self.organization_without_address.name}")

    def test_organization_address_not_deletable(self) -> None:
        """Test Contact.address_block."""
        with self.assertRaises(ProtectedError):
            self.organization.address.delete(hard_delete=True)
