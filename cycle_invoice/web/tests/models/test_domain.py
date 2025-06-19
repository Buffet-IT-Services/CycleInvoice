"""Test cases for the Domain model."""

from django.test import TestCase

from cycle_invoice.contact.tests.models.test_organisation import fake_organisation
from cycle_invoice.web.models import Domain


def fake_domain() -> Domain:
    """Create a fake work type."""
    return Domain(
        name="domain.com",
        customer=fake_organisation(save=True)
    )


class DomainTest(TestCase):
    """Test cases for the Domain model."""

    def test_str(self) -> None:
        """Test the __str__ of Domain."""
        self.assertEqual("domain.com", str(fake_domain()))
