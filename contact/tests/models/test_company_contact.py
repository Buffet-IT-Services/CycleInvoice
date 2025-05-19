"""Test cases for the CompanyContact model."""

from django.test import TestCase

from contact.models import CompanyContact, Contact, Organisation


class CompanyContactTest(TestCase):
    """Test cases for the CompanyContact model."""

    def test_str(self) -> None:
        """Test the __str__ of CompanyContact."""
        contact = Contact.objects.create(first_name="John", last_name="Doe")
        organisation = Organisation.objects.create(name="Test Org")
        company_contact = CompanyContact.objects.create(contact=contact, company=organisation, role="Manager")
        self.assertEqual(str(company_contact), "Test Org - John Doe - Manager")
