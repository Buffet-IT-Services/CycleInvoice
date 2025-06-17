"""Test cases for the Account model."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from cycle_invoice.accounting.models import Account, get_default_buy_account, get_default_sell_account


def fake_account() -> Account:
    """Create a fake account."""
    return \
        Account.objects.get_or_create(name="Test Account", number="1234567890", default_buy=True, default_sell=False)[0]


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

    def test_only_one_default_buy_account(self) -> None:
        """Test that only one account can be set as default buy."""
        acc1 = Account.objects.create(name="A1", number="1", default_buy=True)
        acc2 = Account.objects.create(name="A2", number="2")

        acc2.default_buy = True
        acc2.full_clean()

        self.assertFalse(Account.objects.get(id=acc1.id).default_buy)
        self.assertTrue(acc2.default_buy)

    def test_only_one_default_sell_account(self) -> None:
        """Test that only one account can be set as default sell."""
        acc1 = Account.objects.create(name="A1", number="1", default_sell=True)
        acc2 = Account.objects.create(name="A2", number="2")

        acc2.default_sell = True
        acc2.full_clean()

        self.assertFalse(Account.objects.get(id=acc1.id).default_sell)
        self.assertTrue(acc2.default_sell)

    def test_remove_default_buy_account(self) -> None:
        """Test that you can't remove the default buy."""
        account = Account.objects.create(name="A1", number="1", default_buy=True)

        account.default_buy = False

        with self.assertRaises(ValidationError):
            account.full_clean()

    def test_remove_default_sell_account(self) -> None:
        """Test that you can't remove the default sell."""
        account = Account.objects.create(name="A1", number="1", default_sell=True)

        account.default_sell = False

        with self.assertRaises(ValidationError):
            account.full_clean()

    def test_str(self) -> None:
        """Test the string representation of the account."""
        account = Account.objects.create(name="A1", number="1", default_sell=True)

        self.assertEqual("A1 (1)", str(account))

    def test_get_default_buy_account(self) -> None:
        """Test the get_default_buy_account function."""
        account = Account.objects.create(name="Default Buy Account", number="sys0001", default_buy=True)
        self.assertEqual(account.id, get_default_buy_account())

    def test_get_default_sell_account(self) -> None:
        """Test the get_default_sell_account function."""
        account = Account.objects.create(name="Default Sell Account", number="sys0002", default_sell=True)
        self.assertEqual(account.id, get_default_sell_account())

    def test_get_default_buy_account_create(self) -> None:
        """Test the get_default_buy_account function when no default account exists."""
        Account.objects.all().delete()
        account_id = get_default_buy_account()
        account = Account.objects.get(id=account_id)
        self.assertEqual(account.name, "Default Buy Account")

    def test_get_default_sell_account_create(self) -> None:
        """Test the get_default_sell_account function when no default account exists."""
        Account.objects.all().delete()
        account_id = get_default_sell_account()
        account = Account.objects.get(id=account_id)
        self.assertEqual(account.name, "Default Sell Account")
