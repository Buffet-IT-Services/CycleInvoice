"""Test cases for the CompanyContact model."""

from django.test import TestCase

from contact.models import CompanyContact
from contact.tests.models.test_contact import fake_contact
from contact.tests.models.test_organisation import fake_organisation


class CompanyContactTest(TestCase):
    """Test cases for the CompanyContact model."""

    def test_str(self) -> None:
        """Test the __str__ of CompanyContact."""
        company_contact = CompanyContact.objects.create(
            contact=fake_contact(), company=fake_organisation(), role="Manager"
        )
        self.assertEqual(str(company_contact), "Fake Org - John Doe - Manager")
