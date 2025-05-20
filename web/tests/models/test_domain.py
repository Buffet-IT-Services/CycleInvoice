"""Test cases for the Domain model."""

from django.test import TestCase

from contact.tests.models.test_organisation import fake_organisation
from web.models import Domain


class DomainTest(TestCase):
    """Test cases for the Domain model."""

    def test_str(self) -> None:
        """Test the __str__ of Domain."""
        organisation = fake_organisation()
        domain = Domain.objects.create(name="testdomain.com", customer=organisation)
        self.assertEqual("testdomain.com", str(domain))
