"""Tests for the Model Account"""
from django.test import TestCase
from accounting.models import Account  # Importiere das Modell

class AccountTests(TestCase):

    def test_account_delete_with_default_sell(self):
        # Erstelle ein Beispielkonto mit `default_sell` auf True
        account = Account.objects.create(name="Test Account", default_sell=True)

        # Überprüfe, ob `default_sell` True ist
        self.assertTrue(account.default_sell)

        # Setze `default_sell` auf False
        account.default_sell = False
        account.save()

        # Aktualisiere das Objekt aus der Datenbank und überprüfe, ob `default_sell` False ist
        account.refresh_from_db()
        self.assertFalse(account.default_sell)

