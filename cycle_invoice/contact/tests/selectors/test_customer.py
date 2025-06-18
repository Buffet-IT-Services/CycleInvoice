"""Test cases for selector of customer."""
from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_user
from cycle_invoice.contact.models import Customer
from cycle_invoice.contact.selectors.customer import customer_get, customer_list
from cycle_invoice.contact.tests.models.test_contact import fake_contact
from cycle_invoice.contact.tests.models.test_organisation import fake_organisation


class CustomerTest(TestCase):
    """Test cases for selectors related to Customer."""

    def setUp(self) -> None:
        """Set up test data for Customer selectors."""
        self.user = get_default_user()
        self.contact = fake_contact()
        self.contact.save(user=self.user)
        self.organisation = fake_organisation()
        self.organisation.save(user=self.user)
        self.contact.__class__ = Customer
        self.organisation.__class__ = Customer

    def test_customer_list_returns_all(self) -> None:
        """Test that invoice_list returns all invoices."""
        qs = customer_list()
        self.assertIn(self.contact, qs)
        self.assertIn(self.organisation, qs)
        self.assertEqual(qs.count(), 2)

    def test_customer_get_returns_customer(self) -> None:
        """Test that customer_get returns the correct customer."""
        customer = customer_get(self.contact.id)
        self.assertEqual(customer, self.contact)

    def test_customer_get_returns_none_for_invalid_id(self) -> None:
        """Test that customer_get returns None for an invalid ID."""
        customer = customer_get(99999)
        self.assertIsNone(customer)
