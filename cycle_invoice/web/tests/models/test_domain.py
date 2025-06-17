"""Test cases for the Domain model."""

from django.test import TestCase

from cycle_invoice.contact.tests.models.test_organisation import fake_organisation
from cycle_invoice.web.models import Domain


class DomainTest(TestCase):
    """Test cases for the Domain model."""

    def test_str(self) -> None:
        """Test the __str__ of Domain."""
        organisation = fake_organisation()
        domain = Domain.objects.create(name="domain.com", customer=organisation)
        self.assertEqual("domain.com", str(domain))
