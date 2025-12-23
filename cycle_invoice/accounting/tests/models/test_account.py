"""Tests for the accounting model Account."""

from django.test import TestCase

from cycle_invoice.accounting.tests.factories import AccountFactory


class TestAccount(TestCase):
    """Tests for the accounting model Account."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.account = AccountFactory.create()

    def test_account_str(self) -> None:
        """Test Account.__str__()."""
        self.assertEqual(f"{self.account.name} ({self.account.number})", str(self.account))
