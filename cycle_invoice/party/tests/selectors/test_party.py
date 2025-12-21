"""Test cases for a selector of PArty."""
from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user
from cycle_invoice.party.selectors.party import party_get, party_list
from cycle_invoice.party.tests.factories import OrganizationFactory, ContactFactory


class PartyTest(TestCase):
    """Test cases for selectors related to Party."""

    def setUp(self) -> None:
        """Set up test data for Party selectors."""
        self.user = get_system_user()
        self.organization1 = OrganizationFactory.create()
        self.organization2 = OrganizationFactory.create(soft_deleted=True)
        self.contact1 = ContactFactory.create()
        self.contact2 = ContactFactory.create(soft_deleted=True)

    def test_party_list_returns_active(self) -> None:
        """Test that party_list returns all parties."""
        qs = party_list()
        self.assertIn(self.organization1, qs)
        self.assertNotIn(self.organization2, qs)
        self.assertIn(self.contact1, qs)
        self.assertNotIn(self.contact2, qs)

    def test_party_get_returns_uuid_organization(self) -> None:
        """Test that party_get returns the correct party."""
        party = party_get(self.organization1.uuid)
        self.assertEqual(party, self.organization1)

    def test_party_get_returns_id_organization(self) -> None:
        """Test that party_get returns the correct party."""
        party = party_get(self.organization1.id)
        self.assertEqual(party, self.organization1)

    def test_party_get_returns_uuid_contact(self) -> None:
        """Test that party_get returns the correct party."""
        party = party_get(self.contact1.uuid)
        self.assertEqual(party, self.contact1)

    def test_party_get_returns_id_contact(self) -> None:
        """Test that party_get returns the correct party."""
        party = party_get(self.contact1.id)
        self.assertEqual(party, self.contact1)

    def test_party_get_returns_none_for_invalid_id(self) -> None:
        """Test that party_get returns None for an invalid ID."""
        party = party_get(99999)
        self.assertIsNone(party)
