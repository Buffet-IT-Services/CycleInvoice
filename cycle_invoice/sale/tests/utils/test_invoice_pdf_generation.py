"""Test cases for the Invoice PDF generation utils."""
import hashlib
import os
from io import BytesIO
from unittest.mock import NonCallableMock, patch

from django.http import HttpRequest
from django.test import TestCase
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.contact.tests.models.test_address import fake_address
from cycle_invoice.sale.tests.models.test_document_invoice import fake_document_invoice
from cycle_invoice.sale.tests.models.test_document_item import fake_document_item_product, fake_document_item_work
from cycle_invoice.sale.utils.invoice_pdf_generation import (
    PDFContent,
    add_page_numbers_to_pdf,
    add_pdf_to_storage,
    generate_content,
    generate_html_invoice,
    generate_html_qr_page,
    generate_invoice_pdf,
    generate_pdf_from_html,
)


class InvoicePDFGenerationTest(TestCase):
    """Test cases for the Invoice PDF generation utils."""

    context = {
        "company_info": {
            "company_name": "Test Company Ltd.",
            "company_address": "Test Street 1",
            "company_registration_id": "CHE-123.456.789",
            "company_email": "info@testcompany.com",
            "company_phone": "+41 44 123 45 67",
            "company_website": "www.testcompany.com",
            "zip": "8000",
            "city": "Zurich",
            "country": "Switzerland",
            "company_bank_account": "CH12 3456 7890 1234 5678 9",
        },
        "invoice_details": {
            "total_sum": "100.00",
            "invoice_number": "INV-2024-001",
            "invoice_primary_key": 1,
            "created_date": "01.06.2024",
            "due_date": "30.06.2024",
            "header_text": "Invoice for services",
            "footer_text": "Thank you for your business!",
        },
        "customer": {
            "name": "Max Sample",
            "street": "Customer Road 5",
            "postal_code": "9000",
            "city": "St. Gallen",
            "country": "Switzerland",
            "address_block": "Max Sample\nCustomer Road 5\n9000 St. Gallen\nSwitzerland",
        },
        "show_page_number": False,
        "invoice_items": [
            {
                "product_name": "Consulting",
                "product_description": "IT consulting 2h",
                "quantity": "2.00",
                "price_single": "50.00",
                "discount": "",
                "price_total": "100.00",
            },
            {
                "product_name": "Development",
                "product_description": "Web development 5h",
                "quantity": "5.00",
                "price_single": "20.00",
                "discount": "",
                "price_total": "100.00",
            }
        ],
        "qr_bill_svg": "<svg>QR</svg>"
    }

    def setUp(self) -> None:
        """Set up the test environment with a fake invoice and customer."""
        # Set environment variables for company info
        os.environ["COMPANY_NAME"] = "Test Company Ltd."
        os.environ["COMPANY_ADDRESS"] = "Test Street 1"
        os.environ["COMPANY_REGISTRATION_ID"] = "CHE-123.456.789"
        os.environ["COMPANY_EMAIL"] = "info@testcompany.com"
        os.environ["COMPANY_PHONE"] = "+41 44 123 45 67"
        os.environ["COMPANY_WEBSITE"] = "www.testcompany.com"
        os.environ["COMPANY_ZIP"] = "8000"
        os.environ["COMPANY_CITY"] = "Zurich"
        os.environ["COMPANY_COUNTRY"] = "Switzerland"
        os.environ["COMPANY_BANK_ACCOUNT"] = "CH12 3456 7890 1234 5678 9"

        self.user = get_default_test_user()

        # Create a fake customer and invoice with items
        self.invoice = fake_document_invoice(save=True)
        self.invoice.customer.address = fake_address(save=True)
        self.invoice.customer.save(user=self.user)
        self.item = fake_document_item_product(save=True)
        self.item.invoice = self.invoice
        self.item.save(user=self.user)
        self.item = fake_document_item_work(save=True)
        self.item.invoice = self.invoice
        self.item.save(user=self.user)

    # noinspection DuplicatedCode
    @patch("cycle_invoice.sale.utils.invoice_pdf_generation.generate_swiss_qr")
    def test_generate_content(self, mock_qr: object) -> None:
        """Test that prepare_invoice_context returns the expected dictionary."""
        mock_qr.side_effect = lambda ctx: ctx.update({"qr_bill_svg": "<svg>QR</svg>"})
        context = generate_content(self.invoice.pk)

        # check company info
        self.assertEqual("Test Company Ltd.", context["company_info"]["company_name"])
        self.assertEqual("Test Street 1", context["company_info"]["company_address"])
        self.assertEqual("CHE-123.456.789", context["company_info"]["company_registration_id"])
        self.assertEqual("info@testcompany.com", context["company_info"]["company_email"])
        self.assertEqual("+41 44 123 45 67", context["company_info"]["company_phone"])
        self.assertEqual("www.testcompany.com", context["company_info"]["company_website"])
        self.assertEqual("8000", context["company_info"]["zip"])
        self.assertEqual("Zurich", context["company_info"]["city"])
        self.assertEqual("Switzerland", context["company_info"]["country"])
        self.assertEqual("CH12 3456 7890 1234 5678 9", context["company_info"]["company_bank_account"])

        # check invoice details
        self.assertEqual(context["invoice_details"]["total_sum"], str(self.invoice.total_sum))
        self.assertEqual(context["invoice_details"]["invoice_number"], self.invoice.invoice_number)
        self.assertEqual(context["invoice_details"]["invoice_primary_key"], self.invoice.pk)
        self.assertEqual(context["invoice_details"]["created_date"], self.invoice.date.strftime("%d.%m.%Y"))
        self.assertEqual(context["invoice_details"]["due_date"], self.invoice.due_date.strftime("%d.%m.%Y"))
        self.assertEqual(context["invoice_details"]["header_text"], self.invoice.header_text)
        self.assertEqual(context["invoice_details"]["footer_text"], self.invoice.footer_text)

        # check customer details
        self.assertEqual(context["customer"]["name"], str(self.invoice.customer))
        self.assertEqual(context["customer"]["street"],
                         f"{self.invoice.customer.address.street} {self.invoice.customer.address.number}")
        self.assertEqual(context["customer"]["postal_code"], self.invoice.customer.address.zip_code)
        self.assertEqual(context["customer"]["city"], self.invoice.customer.address.city)
        self.assertEqual(context["customer"]["country"], self.invoice.customer.address.country)
        self.assertEqual(context["customer"]["address_block"], self.invoice.customer.address_block)

        # check invoice items
        self.assertEqual(len(context["invoice_items"]), 2)
        self.assertEqual(context["invoice_items"][1]["product_name"], self.item.title)
        self.assertEqual(context["invoice_items"][1]["product_description"], self.item.description)
        self.assertEqual(context["invoice_items"][1]["quantity"], self.item.quantity_str)
        self.assertEqual(context["invoice_items"][1]["price_single"], self.item.price_str)
        self.assertEqual(context["invoice_items"][1]["discount"], self.item.discount_str)
        self.assertEqual(context["invoice_items"][1]["price_total"], self.item.total_str)

        # check miscellaneous
        self.assertFalse(context["show_page_number"])
        self.assertEqual("<svg>QR</svg>", context["qr_bill_svg"])

    def test_generate_html_invoice(self) -> None:
        """Test that generate_html_invoice renders the invoice HTML template with context."""
        html = generate_html_invoice(self.context)
        html_hash = hashlib.sha256(html.encode()).hexdigest()
        self.assertIsInstance(html, str)
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertEqual("f359a8bdb72a7e54cc7c3ff7eddbb875a89e5ab49d288f47b76bf393dd872985", html_hash)

    def test_generate_html_qr_page(self) -> None:
        """Test that generate_html_qr_page returns the expected HTML for the QR bill."""
        html = generate_html_qr_page(self.context)
        html_hash = hashlib.sha256(html.encode()).hexdigest()
        self.assertIsInstance(html, str)
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertEqual("e6aa4a5590a7734fd58148e214bee49285d4d3199482dab18241c85855bcf160", html_hash)

    def test_generate_pdf_from_html(self) -> None:
        """Test that generate_pdf_from_html returns PDF bytes for valid HTML input."""
        html = "<html><body><h1>Test PDF</h1><p>Page 1</p></body></html>"
        base_url = "http://testserver/"
        pdf_bytes = generate_pdf_from_html(html, base_url)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 100)  # Should be a non-trivial PDF
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

    def test_add_page_numbers_to_pdf(self) -> None:
        """Test that add_page_numbers_to_pdf adds page numbers to a PDF."""
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.drawString(100, 750, "Seite 1")
        c.showPage()
        c.drawString(100, 750, "Seite 2")
        c.save()
        buffer.seek(0)
        pdf_bytes = buffer.getvalue()

        # Test the function
        numbered_pdf_stream = add_page_numbers_to_pdf(pdf_bytes)
        numbered_pdf_stream.seek(0)
        reader = PdfReader(numbered_pdf_stream)
        self.assertEqual(len(reader.pages), 2)

        # Check that the page structure is preserved and page numbers are added
        text_page1 = reader.pages[0].extract_text()
        text_page2 = reader.pages[1].extract_text()
        self.assertIn("Seite 1", text_page1)
        self.assertIn("Seite 2", text_page2)
        self.assertIn("Seite 1 von 2", text_page1)
        self.assertIn("Seite 2 von 2", text_page2)

    @patch("cycle_invoice.sale.utils.invoice_pdf_generation.generate_content")
    @patch("cycle_invoice.sale.utils.invoice_pdf_generation.generate_html_invoice")
    @patch("cycle_invoice.sale.utils.invoice_pdf_generation.generate_html_qr_page")
    @patch("cycle_invoice.sale.utils.invoice_pdf_generation.generate_pdf_from_html")
    @patch("cycle_invoice.sale.utils.invoice_pdf_generation.add_page_numbers_to_pdf")
    def test_generate_invoice_pdf_two_pass(self, mock_add_page_numbers: NonCallableMock,
                                           mock_generate_pdf_from_html: NonCallableMock,
                                           mock_generate_html_qr_page: NonCallableMock,
                                           mock_generate_html_invoice: NonCallableMock,
                                           mock_generate_content: NonCallableMock) -> None:
        """Test that generate_invoice_pdf_two_pass returns a PDFContent object with correct filename and PDF bytes."""

        # Create a valid PDF for mocking
        def create_valid_pdf_bytes(text: str = "Test PDF") -> bytes:
            """
            Create a simple PDF with the given text.

            :param text:  Text to include in the PDF
            :return:  Bytes of the generated PDF
            """
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            c.drawString(100, 750, text)
            c.showPage()
            c.save()
            buffer.seek(0)
            return buffer.getvalue()

        valid_pdf_invoice = create_valid_pdf_bytes("Invoice")
        valid_pdf_qr = create_valid_pdf_bytes("QR")

        # Mock content and HTML
        mock_generate_content.return_value = {"qr_bill_svg": "<svg>QR</svg>"}
        mock_generate_html_invoice.return_value = "<html>Invoice</html>"
        mock_generate_html_qr_page.return_value = "<html>QR</html>"
        mock_generate_pdf_from_html.side_effect = [valid_pdf_invoice, valid_pdf_qr]
        mock_add_page_numbers.return_value = BytesIO(valid_pdf_invoice)

        # Prepare request
        request = HttpRequest()
        request.build_absolute_uri = lambda path="/": f"https://testserver{path}"

        # Call the function
        generate_invoice_pdf(request, 42)

        # Check mocks called as expected
        mock_generate_content.assert_called_once_with(42)
        mock_generate_html_invoice.assert_called_once()
        mock_generate_html_qr_page.assert_called_once()
        self.assertEqual(mock_generate_pdf_from_html.call_count, 2)
        mock_add_page_numbers.assert_called_once()

    @patch("cycle_invoice.sale.utils.invoice_pdf_generation.default_storage")
    @patch("cycle_invoice.sale.utils.invoice_pdf_generation.ContentFile")
    def test_add_pdf_to_storage(self, mock_content_file: NonCallableMock,
                                mock_default_storage: NonCallableMock) -> None:
        """Test that add_pdf_to_storage saves the PDF to default storage with correct filename and content."""
        # Prepare PDFContent
        pdf_content = PDFContent(content=b"PDFDATA", filename="test_invoice.pdf")
        # Call the function
        add_pdf_to_storage(pdf_content)
        # Check ContentFile called with correct content
        mock_content_file.assert_called_once_with(b"PDFDATA")
        # Check default_storage.save called with correct filename and ContentFile
        mock_default_storage.save.assert_called_once()
        args, kwargs = mock_default_storage.save.call_args
        self.assertEqual(args[0], "test_invoice.pdf")
        self.assertIs(args[1], mock_content_file.return_value)
