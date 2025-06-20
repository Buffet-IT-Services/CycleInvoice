"""Test cases for the Organisation model."""

from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.contact.models import Organisation


def fake_organisation(
        save: bool,
) -> Organisation:
    """Create a fake organisation."""
    organisation = Organisation(
        name="Fake Org"
    )
    if save:
        organisation.save(user=get_default_test_user())
    return organisation


def fake_organisation_with_name(
        name: str,
        save: bool,
) -> Organisation:
    """Create a fake organisation with custom name."""
    organisation = Organisation(
        name=name
    )
    if save:
        organisation.save(user=get_default_test_user())
    return organisation


class OrganisationTest(TestCase):
    """Test cases for the Organisation model."""

    def test_str(self) -> None:
        """Test the __str__ of organisation."""
        self.assertEqual(str(fake_organisation(save=False)), "Fake Org")
