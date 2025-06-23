"""Tests for the DocumentInvoice API."""
from django.test import TestCase
from django.urls import reverse

from cycle_invoice.api.tests.base import token_admin_create, token_norights_create, token_user_create
from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.contact.tests.models.test_contact import fake_contact
from cycle_invoice.sale.selectors.document_invoice import invoice_get
from cycle_invoice.sale.tests.models.test_document_invoice import (
    fake_document_invoice,
    fake_document_invoice_with_invoice_number,
)


class InvoiceListApiTest(TestCase):
    """Test cases for the InvoiceListApi."""

    def setUp(self) -> None:
        """Set up test data."""
        self.invoice1 = fake_document_invoice(save=True)
        self.invoice2 = fake_document_invoice_with_invoice_number(invoice_number="INV-2", save=True)
        self.user = get_default_test_user()

        self.token_admin = token_admin_create(self.client)
        self.token_norights = token_norights_create(self.client)
        self.url = reverse("document-invoice-list")

    def test_get_invoices_with_admin(self) -> None:
        """Test GET request returns invoices without any filters set."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["results"]), 2)
        self.assertEqual(self.invoice1.uuid.__str__(), data["results"][0]["uuid"])
        self.assertEqual(self.invoice1.customer.uuid.__str__(), data["results"][0]["customer"])
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
        self.invoice = fake_document_invoice(save=True)
        self.token_admin = token_admin_create(self.client)
        self.token_norights = token_norights_create(self.client)
        self.url = reverse("document-invoice-detail", kwargs={"invoice_uuid": self.invoice.uuid})

    def test_get_invoice_with_admin(self) -> None:
        """Test GET request returns the invoice with all details."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data["uuid"], str)
        self.assertEqual(self.invoice.invoice_number, data["invoice_number"])
        self.assertEqual(self.invoice.date.isoformat(), data["date"])
        self.assertEqual(self.invoice.due_date.isoformat(), data["due_date"])
        self.assertEqual(self.invoice.header_text, data["header_text"])
        self.assertEqual(self.invoice.footer_text, data["footer_text"])
        self.assertEqual(self.invoice.customer.__str__(), data["customer"]["name"])

        # Make sure only expected fields are returned
        self.assertSetEqual(set(data.keys()),
                            {"uuid", "invoice_number", "date", "due_date", "header_text", "footer_text", "customer",
                             "created_by", "created_at", "updated_by", "updated_at"})
        self.assertEqual(set(data["customer"].keys()), {"uuid", "name"})

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
        invalid_url = reverse("document-invoice-detail",
                              kwargs={"invoice_uuid": "4398f182-3c41-480a-afc7-15387ce5511c"})
        response = self.client.get(invalid_url, HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        self.assertEqual(response.status_code, 404)


class InvoiceCreateApiTest(TestCase):
    """Test cases for the InvoiceCreateApi."""

    def setUp(self) -> None:
        """Set up test data."""
        self.token_admin = token_admin_create(self.client)
        self.token_norights = token_norights_create(self.client)
        self.url = reverse("document-invoice-create")
        self.customer = fake_contact(save=True)
        self.content = {
            "invoice_number": "INV-12345",
            "date": "2023-10-01",
            "due_date": "2023-10-15",
            "header_text": "Header Text",
            "footer_text": "Footer Text",
            "customer": self.customer.id
        }

    def test_post_admin_returns_invoice_details(self) -> None:
        """Test POST request as admin returns the invoice with all details."""
        response = self.client.post(
            self.url,
            self.content,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}"
        )
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(data["uuid"], str)
        self.assertEqual(self.content["invoice_number"], data["invoice_number"])
        self.assertEqual(self.content["date"], data["date"])
        self.assertEqual(self.content["due_date"], data["due_date"])
        self.assertEqual(self.content["header_text"], data["header_text"])
        self.assertEqual(self.content["footer_text"], data["footer_text"])
        self.assertEqual(self.customer.__str__(), data["customer"]["name"])
        self.assertSetEqual(set(data.keys()),
                            {"uuid", "invoice_number", "date", "due_date", "header_text", "footer_text", "customer",
                             "created_by", "created_at", "updated_by", "updated_at"})
        self.assertEqual(set(data["customer"].keys()), {"uuid", "name"})

    def test_post_with_rights_returns_201(self) -> None:
        """Test POST request with add_documentinvoice permission returns 201."""
        token = token_user_create(self.client, permissions=["add_documentinvoice"])
        response = self.client.post(self.url, self.content, content_type="application/json",
                                    HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, 201)

    def test_post_no_rights_returns_403(self) -> None:
        """Test POST request without permissions returns 403 Forbidden."""
        response = self.client.post(self.url, self.content, content_type="application/json",
                                    HTTP_AUTHORIZATION=f"Bearer {self.token_norights}")
        self.assertEqual(response.status_code, 403)

    def test_post_existing_invoice_number_returns_400(self) -> None:
        """Test POST request with an existing invoice number returns 400 Bad Request."""
        fake_document_invoice_with_invoice_number(self.content["invoice_number"], save=True)
        response = self.client.post(
            self.url,
            self.content,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}"
        )
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_date_returns_400(self) -> None:
        """Test POST request with an invalid date format returns 400 Bad Request."""
        invalid_content = self.content.copy()
        invalid_content["date"] = "invalid-date"
        response = self.client.post(
            self.url,
            invalid_content,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}"
        )
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_due_date_returns_400(self) -> None:
        """Test POST request with an invalid due date format returns 400 Bad Request."""
        invalid_content = self.content.copy()
        invalid_content["due_date"] = "invalid-date"
        response = self.client.post(
            self.url,
            invalid_content,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}"
        )
        self.assertEqual(response.status_code, 400)

    def test_post_missing_fields_returns_400(self) -> None:
        """Test POST request with missing required fields returns 400 Bad Request."""
        incomplete_content = self.content.copy()
        del incomplete_content["invoice_number"]
        response = self.client.post(
            self.url,
            incomplete_content,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}"
        )
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_customer_returns_400(self) -> None:
        """Test POST request with an invalid customer ID returns 400 Bad Request."""
        invalid_content = self.content.copy()
        invalid_content["customer"] = 9999
        response = self.client.post(
            self.url,
            invalid_content,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}"
        )
        self.assertEqual(response.status_code, 400)

    def test_post_without_header_and_footer_returns_201(self) -> None:
        """Test POST request without header and footer text returns 201 and empty fields."""
        content_without_header_footer = self.content.copy()
        del content_without_header_footer["header_text"]
        del content_without_header_footer["footer_text"]
        response = self.client.post(
            self.url,
            content_without_header_footer,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}"
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual("", data["header_text"])
        self.assertEqual("", data["footer_text"])


class InvoiceUpdateApiTest(TestCase):
    """Test cases for the InvoiceUpdateApi."""

    def setUp(self) -> None:
        """Set up test data."""
        self.token_admin = token_admin_create(self.client)
        self.token_norights = token_norights_create(self.client)
        self.invoice = fake_document_invoice(save=True)
        self.url = reverse("document-invoice-update", kwargs={"invoice_uuid": self.invoice.uuid})

    def test_patch_invoice_with_admin(self) -> None:
        """Test PATCH request returns the updated invoice."""
        content = {"invoice_number": "INV-12345-UPDATED"}
        response = self.client.patch(self.url, content, content_type="application/json",
                                     HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")

        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual("INV-12345-UPDATED", data["invoice_number"])

        # Make sure only expected fields are returned
        self.assertSetEqual(set(data.keys()),
                            {"uuid", "invoice_number", "date", "due_date", "header_text", "footer_text", "customer",
                             "created_by", "created_at", "updated_by", "updated_at"})
        self.assertEqual(set(data["customer"].keys()), {"uuid", "name"})

    def test_get_invoice_with_rights(self) -> None:
        """Test PATCH request with specific permissions."""
        token = token_user_create(self.client, permissions=["change_documentinvoice"])
        content = {"invoice_number": "INV-12345-UPDATED"}
        response = self.client.patch(self.url, content, content_type="application/json",
                                     HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, 201)

    def test_get_invoice_with_no_rights(self) -> None:
        """Test PATCH request returns 403 Forbidden without permissions."""
        content = {"invoice_number": "INV-12345-UPDATED"}
        response = self.client.patch(self.url, content, content_type="application/json",
                                     HTTP_AUTHORIZATION=f"Bearer {self.token_norights}")
        self.assertEqual(response.status_code, 403)

    def test_add_invoice_with_existing_invoice_number(self) -> None:
        """Test PATCH request with an existing invoice number returns 400 Bad Request."""
        fake_document_invoice_with_invoice_number(invoice_number="INV-12345-NEW", save=True)
        content = {"invoice_number": "INV-12345-NEW"}
        response = self.client.patch(self.url, content, content_type="application/json",
                                     HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        self.assertEqual(response.status_code, 400)

    def test_add_invoice_with_previous_invoice_number(self) -> None:
        """Test PATCH request with the current invoice number returns the updated invoice."""
        content = {"invoice_number": self.invoice.invoice_number, "footer_text": "Updated Footer"}
        response = self.client.patch(self.url, content, content_type="application/json",
                                     HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        content = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(content["invoice_number"], self.invoice.invoice_number)
        self.assertEqual(content["footer_text"], "Updated Footer")

    def test_add_invoice_with_invalid_date(self) -> None:
        """Test PATCH request with an invalid date format returns 400 Bad Request."""
        content = {"date": "invalid-date"}
        response = self.client.patch(self.url, content, content_type="application/json",
                                     HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        self.assertEqual(response.status_code, 400)

    def test_patch_invalid_due_date_returns_400(self) -> None:
        """Test PATCH request with an invalid due date format returns 400 Bad Request."""
        content = {"due_date": "invalid-date"}
        response = self.client.patch(self.url, content, content_type="application/json",
                                     HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        self.assertEqual(response.status_code, 400)

    def test_patch_invalid_customer_returns_400(self) -> None:
        """Test PATCH request with an invalid customer ID returns 400 Bad Request."""
        content = {"customer": "9999"}
        response = self.client.patch(self.url, content, content_type="application/json",
                                     HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        self.assertEqual(response.status_code, 400)

    def test_patch_valid_customer_returns_201(self) -> None:
        """Test PATCH request with a valid customer ID returns 201 Success."""
        contact = fake_contact(save=True)
        content = {"customer": contact.id}
        response = self.client.patch(self.url, content, content_type="application/json",
                                     HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        self.assertEqual(response.status_code, 201)

    def test_patch_invalid_invoice_returns_404(self) -> None:
        """Test PATCH request with an invalid invoice ID returns 404 Not Found."""
        url = reverse("document-invoice-update", kwargs={"invoice_uuid": "4398f182-3c41-480a-afc7-15387ce5511c"})
        content = {"invoice_number": "INV-12345-UPDATED"}
        response = self.client.patch(url, content, content_type="application/json",
                                     HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        self.assertEqual(response.status_code, 404)


class InvoiceDeleteApiTest(TestCase):
    """Test cases for the InvoiceDeleteApi."""

    def setUp(self) -> None:
        """Set up test data."""
        self.token_admin = token_admin_create(self.client)
        self.token_rights = token_user_create(self.client, permissions=["delete_documentinvoice"])
        self.token_norights = token_norights_create(self.client)
        self.invoice = fake_document_invoice(save=True)
        self.url = reverse("document-invoice-delete", kwargs={"invoice_uuid": self.invoice.uuid})

    def test_delete_invoice_with_admin(self) -> None:
        """Test DELETE request returns the updated invoice."""
        updated_before = self.invoice.updated_at
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")

        self.assertEqual(response.status_code, 204)
        self.invoice.refresh_from_db()  # Refresh the invoice instance from the database
        self.assertTrue(self.invoice.soft_deleted)
        self.assertNotEqual(self.invoice.updated_at, updated_before)

    def test_delete_invoice_with_rights(self) -> None:
        """Test DELETE request with specific permissions."""
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token_rights}")

        self.assertEqual(response.status_code, 204)
        self.invoice.refresh_from_db()  # Refresh the invoice instance from the database
        self.assertTrue(self.invoice.soft_deleted)

    def test_delete_invoice_with_no_rights(self) -> None:
        """Test DELETE request returns 403 Forbidden without permissions."""
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token_norights}")
        self.assertEqual(response.status_code, 403)

    def test_delete_invalid_invoice_returns_404(self) -> None:
        """Test DELETE request with an invalid invoice ID returns 404 Not Found."""
        url = reverse("document-invoice-delete", kwargs={"invoice_uuid": "4398f182-3c41-480a-afc7-15387ce5511c"})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        self.assertEqual(response.status_code, 404)

    def test_delete_invoice_with_admin_hard(self) -> None:
        """Test DELETE request returns the updated invoice."""
        content = {"hard_delete": True}
        response = self.client.delete(self.url, content, content_type="application/json",
                                      HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(invoice_get(invoice_id=self.invoice.uuid.__str__()))

    def test_delete_invoice_with_rights_hard(self) -> None:
        """Test DELETE request returns the updated invoice."""
        content = {"hard_delete": True}
        response = self.client.delete(self.url, content, content_type="application/json",
                                      HTTP_AUTHORIZATION=f"Bearer {self.token_rights}")

        self.assertEqual(response.status_code, 403)
        self.invoice.refresh_from_db()  # Refresh the invoice instance from the database
        self.assertFalse(self.invoice.soft_deleted)
        self.assertIsNotNone(invoice_get(invoice_id=self.invoice.uuid.__str__()))
