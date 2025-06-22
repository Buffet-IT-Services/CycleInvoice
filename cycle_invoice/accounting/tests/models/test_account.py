"""Tests for the Account model."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from cycle_invoice.accounting.models import Account, get_default_buy_account, get_default_sell_account
from cycle_invoice.common.selectors import get_object
from cycle_invoice.common.tests.base import get_default_test_user


def fake_account(
        save: bool,  # noqa: FBT001
        default_buy: bool = False,  # noqa: FBT001,FBT002
        default_sell: bool = False,  # noqa: FBT001,FBT002
) -> Account:
    """Create a fake account."""
    account = get_object(
        Account,
        number="1234567890",
    )
    if account is None:
        account = Account(
            name="Test Account",
            number="1234567890",
            default_buy=default_buy,
            default_sell=default_sell,
        )
        if save:
            account.save(user=get_default_test_user())
    return account


class AccountTest(TestCase):
    """Test cases for the Account model."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user = get_default_test_user()

    def test_prevent_default_buy_deletion(self) -> None:
        """Test that default buy account cannot be deleted."""
        account = fake_account(
            save=True,
            default_buy=True,
        )
        with self.assertRaises(ValidationError):
            # TODO: Fix this ugly workaround for the hard delete issue
            # https://github.com/Buffet-IT-Services/CycleInvoice/issues/66
            # Issue URL: https://github.com/Buffet-IT-Services/CycleInvoice/issues/66
            account.delete(user=self.user, hard_delete=True)

    def test_prevent_default_sell_deletion(self) -> None:
        """Test that default sell account cannot be deleted."""
        account = fake_account(
            save=True,
            default_sell=True,
        )
        with self.assertRaises(ValidationError):
            # TODO: Fix this ugly workaround for the hard delete issue
            # https://github.com/Buffet-IT-Services/CycleInvoice/issues/65
            # Issue URL: https://github.com/Buffet-IT-Services/CycleInvoice/issues/65
            account.delete(user=self.user, hard_delete=True)

    # noinspection DuplicatedCode
    def test_only_one_default_buy_account(self) -> None:
        """Test that only one account can be set as default buy."""
        account1 = fake_account(
            save=True,
            default_buy=True,
        )

        account2 = Account(
            name="Test Account 2",
            number="0987654321",
        )
        account2.save(user=self.user)

        account2.default_buy = True
        account2.full_clean()
        account2.save(user=self.user)

        account1.refresh_from_db()
        account2.refresh_from_db()

        self.assertFalse(account1.default_buy)
        self.assertTrue(account2.default_buy)

    # noinspection DuplicatedCode
    def test_only_one_default_sell_account(self) -> None:
        """Test that only one account can be set as default sell."""
        account1 = fake_account(
            save=True,
            default_sell=True,
        )
        account2 = Account(
            name="Test Account 2",
            number="0987654321",
        )
        account2.save(user=self.user)

        account2.default_sell = True
        account2.full_clean()
        account2.save(user=self.user)

        account1.refresh_from_db()
        account2.refresh_from_db()

        self.assertFalse(account1.default_sell)
        self.assertTrue(account2.default_sell)

    def test_remove_default_buy_account(self) -> None:
        """Test that you can't remove the default buy."""
        account = fake_account(
            save=True,
            default_buy=True,
        )

        account.default_buy = False

        with self.assertRaises(ValidationError):
            account.full_clean()

    def test_remove_default_sell_account(self) -> None:
        """Test that you can't remove the default sell."""
        account = fake_account(
            save=True,
            default_sell=True,
        )

        account.default_sell = False

        with self.assertRaises(ValidationError):
            account.full_clean()

    def test_str(self) -> None:
        """Test the string representation of the account."""
        self.assertEqual("Test Account (1234567890)", str(fake_account(save=False)))

    def test_get_default_buy_account(self) -> None:
        """Test the get_default_buy_account function."""
        account = fake_account(
            save=True,
            default_buy=True,
        )

        self.assertEqual(account.id, get_default_buy_account())

    def test_get_default_sell_account(self) -> None:
        """Test the get_default_sell_account function."""
        account = fake_account(
            save=True,
            default_sell=True,
        )

        self.assertEqual(account.id, get_default_sell_account())

    def test_get_default_buy_account_create(self) -> None:
        """Test the get_default_buy_account function when no default account exists."""
        account_id = get_default_buy_account()
        account = get_object(Account, id=account_id)
        self.assertEqual(account.name, "Default Buy Account")

    def test_get_default_sell_account_create(self) -> None:
        """Test the get_default_sell_account function when no default account exists."""
        account_id = get_default_sell_account()
        account = get_object(Account, id=account_id)
        self.assertEqual(account.name, "Default Sell Account")
