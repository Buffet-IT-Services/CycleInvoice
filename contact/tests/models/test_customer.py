"""Test cases for the Customer model."""
from django.test import TestCase

from contact.models import Contact


class CustomerTest(TestCase):
    """Test cases for the Customer model."""

    def test_str(self) -> None:
        """Test the __str__ of organisation."""

        contact = Contact.objects.create(first_name="John", last_name="Doe")
        self.assertEqual(str(contact), "John Doe")