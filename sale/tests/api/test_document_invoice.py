"""Tests for the DocumentInvoice API."""
from django.test import TestCase
from django.urls import reverse

from api.tests.base import token_admin_create, token_user_create, token_norights_create
from sale.tests.models.test_document_invoice import fake_document_invoice


class InvoiceListApiTest(TestCase):
    """Test cases for the InvoiceListApi."""

    def setUp(self):
        """Set up test data."""
        fake_document_invoice()
        self.token_admin = token_admin_create(self.client)
        self.token_norights = token_norights_create(self.client)
        self.url = reverse('document-invoice-list')

    def test_get_invoices_with_admin(self):
        """Test GET request returns invoices without any filters set."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual("INV-12345", data['results'][0]['invoice_number'])

    def test_get_invoices_with_rights(self) -> None:
        """Test GET request returns invoices with specific permissions."""
        token = token_user_create(self.client, permissions=["view_documentinvoice"])
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, 200)

    def test_get_invoices_with_no_rights(self) -> None:
        """Test GET request returns 403 Forbidden without permissions."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token_norights}")
        self.assertEqual(response.status_code, 403)

