"""Test cases for the CompanyContact model."""

from django.test import TestCase

from cycle_invoice.contact.models import CompanyContact
from cycle_invoice.contact.tests.models.test_contact import fake_contact
from cycle_invoice.contact.tests.models.test_organisation import fake_organisation


class CompanyContactTest(TestCase):
    """Test cases for the CompanyContact model."""

    def test_str(self) -> None:
        """Test the __str__ of CompanyContact."""
        company_contact = CompanyContact(
            contact=fake_contact(save=True),
            company=fake_organisation(save=True),
            role="Manager"
        )
        self.assertEqual(str(company_contact), "Fake Org - John Doe - Manager")
