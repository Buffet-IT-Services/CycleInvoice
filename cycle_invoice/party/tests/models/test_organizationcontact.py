"""Tests for the party model OrganizationContact."""
from django.db import IntegrityError
from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.party.models import OrganizationContact
from cycle_invoice.party.tests.factories import OrganizationContactFactory


class TestOrganizationContact(TestCase):
    """Tests for the party model OrganizationContact."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.user = get_system_user()
        self.oc = OrganizationContactFactory.create()

    def test_organization_contact_str(self) -> None:
        """Test OrganizationContact.__str__()."""
        self.assertEqual(str(self.oc), f"{self.oc.organization} - {self.oc.contact} - {self.oc.role}")

    def test_organization_contact_unique_together(self) -> None:
        """Test OrganizationContact unique together constraint."""
        with self.assertRaises(IntegrityError):
            OrganizationContactFactory.create(organization=self.oc.organization, contact=self.oc.contact)

    def test_organization_contact_cascade_delete_organization(self) -> None:
        """Test OrganizationContact cascade delete organization."""
        self.oc.organization.delete(hard_delete=True, user=self.user)
        self.assertFalse(OrganizationContact.objects.exists())

    def test_organization_contact_cascade_delete_contact(self) -> None:
        """Test OrganizationContact cascade delete contact."""
        self.oc.contact.delete(hard_delete=True, user=self.user)
        self.assertFalse(OrganizationContact.objects.exists())
