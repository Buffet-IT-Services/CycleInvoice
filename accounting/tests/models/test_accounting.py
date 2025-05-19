"""Test cases for the Account model."""
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounting.models import Account


class AccountTest(TestCase):
    """Test cases for the Account model."""

    def test_prevent_default_sell_deletion(self) -> None:
        """Test that default sell account cannot be deleted."""
        account = Account.objects.create(name="Test", number="123", default_sell=True)
        with self.assertRaises(ValidationError):
            account.delete()

    def test_prevent_default_buy_deletion(self) -> None:
        """Test that default buy account cannot be deleted."""
        account = Account.objects.create(name="Test", number="123", default_buy=True)
        with self.assertRaises(ValidationError):
            account.delete()
