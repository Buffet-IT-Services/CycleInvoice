"""Tests for the DocumentInvoice API."""
from django.test import TestCase
from django.urls import reverse

from api.tests.base import token_admin_create, token_norights_create, token_user_create
from sale.tests.models.test_document_invoice import fake_document_invoice, fake_document_invoice_with_invoice_number


class InvoiceListApiTest(TestCase):
    """Test cases for the InvoiceListApi."""

    def setUp(self) -> None:
        """Set up test data."""
        self.invoice1 = fake_document_invoice()
        self.invoice2 = fake_document_invoice_with_invoice_number("INV-2")
        self.token_admin = token_admin_create(self.client)
        self.token_norights = token_norights_create(self.client)
        self.url = reverse("document-invoice-list")

    def test_get_invoices_with_admin(self) -> None:
        """Test GET request returns invoices without any filters set."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["results"]), 2)
        self.assertEqual(self.invoice1.id, data["results"][0]["id"])
        self.assertEqual(self.invoice1.customer.id, data["results"][0]["customer"])
        self.assertEqual(self.invoice1.invoice_number, data["results"][0]["invoice_number"])
        self.assertEqual(self.invoice1.date.isoformat(), data["results"][0]["date"])
        self.assertEqual(self.invoice1.due_date.isoformat(), data["results"][0]["due_date"])
        self.assertEqual(self.invoice2.invoice_number, data["results"][1]["invoice_number"])

    def test_get_invoices_with_rights(self) -> None:
        """Test GET request returns invoices with specific permissions."""
        token = token_user_create(self.client, permissions=["view_documentinvoice"])
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, 200)

    def test_get_invoices_with_no_rights(self) -> None:
        """Test GET request returns 403 Forbidden without permissions."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token_norights}")
        self.assertEqual(response.status_code, 403)

    def test_get_invoices_with_filters(self) -> None:
        """Test GET request with filters applied."""
        response = self.client.get(
            self.url,
            {"invoice_number": "INV-2"},
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}"
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(data["results"]))


class InvoiceDetailApiTest(TestCase):
    """Test cases for the InvoiceDetailApi."""

    def setUp(self) -> None:
        """Set up test data."""
        self.invoice = fake_document_invoice()
        self.token_admin = token_admin_create(self.client)
        self.token_norights = token_norights_create(self.client)
        self.url = reverse("document-invoice-detail", kwargs={"pk": self.invoice.id})

    def test_get_invoice_with_admin(self) -> None:
        """Test GET request returns the invoice with all details."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.invoice.id, data["id"])
        self.assertEqual(self.invoice.invoice_number, data["invoice_number"])
        self.assertEqual(self.invoice.date.isoformat(), data["date"])
        self.assertEqual(self.invoice.due_date.isoformat(), data["due_date"])
        self.assertEqual(self.invoice.header_text, data["header_text"])
        self.assertEqual(self.invoice.footer_text, data["footer_text"])
        self.assertEqual(self.invoice.customer.id, data["customer"]["id"])
        self.assertEqual(self.invoice.customer.__str__(), data["customer"]["name"])

        # Make sure only expected fields are returned
        self.assertSetEqual(set(data.keys()),
                            {"id", "invoice_number", "date", "due_date", "header_text", "footer_text", "customer"})

    def test_get_invoice_with_rights(self) -> None:
        """Test GET request returns invoices with specific permissions."""
        token = token_user_create(self.client, permissions=["view_documentinvoice"])
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, 200)

    def test_get_invoice_with_no_rights(self) -> None:
        """Test GET request returns 403 Forbidden without permissions."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token_norights}")
        self.assertEqual(response.status_code, 403)

    def test_get_invoice_with_invalid_id(self) -> None:
        """Test GET request with an invalid invoice ID returns 404 Not Found."""
        invalid_url = reverse("document-invoice-detail", kwargs={"pk": 9999})
        response = self.client.get(invalid_url, HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        self.assertEqual(response.status_code, 404)
