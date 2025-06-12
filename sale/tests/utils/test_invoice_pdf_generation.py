"""Test cases for the Invoice PDF generation utils."""
import hashlib
import os
from unittest.mock import patch

from django.test import TestCase

from contact.tests.models.test_address import fake_address
from contact.tests.models.test_contact import fake_contact
from sale.tests.models.test_document_invoice import fake_document_invoice
from sale.tests.models.test_document_item import fake_document_item_product, fake_document_item_work
from sale.utils.invoice_pdf_generation import generate_content


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

    def setUp(self):
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

        # Create a fake customer and invoice with items
        self.customer = fake_contact()
        self.customer.address = fake_address()
        self.customer.save()
        self.invoice = fake_document_invoice()
        self.invoice.customer = self.customer
        self.invoice.save()
        self.item = fake_document_item_product()
        self.item.invoice = self.invoice
        self.item.save()
        self.item = fake_document_item_work()
        self.item.invoice = self.invoice
        self.item.save()

    # noinspection DuplicatedCode
    @patch("sale.utils.invoice_pdf_generation.generate_swiss_qr")
    def test_prepare_invoice_context_returns_expected_dict(self, mock_qr) -> None:
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
        self.assertEqual(context["customer"]["name"], str(self.customer))
        self.assertEqual(context["customer"]["street"],
                         f"{self.customer.address.street} {self.customer.address.number}")
        self.assertEqual(context["customer"]["postal_code"], self.customer.address.zip_code)
        self.assertEqual(context["customer"]["city"], self.customer.address.city)
        self.assertEqual(context["customer"]["country"], self.customer.address.country)
        self.assertEqual(context["customer"]["address_block"], self.customer.address_block)

        # check invoice items
        self.assertEqual(len(context["invoice_items"]), 2)
        self.assertEqual(context["invoice_items"][1]["product_name"], self.item.title)
        self.assertEqual(context["invoice_items"][1]["product_description"], self.item.description)
        self.assertEqual(context["invoice_items"][1]["quantity"], "2.00")  # TODO: Adjust to dynamic quantity
        self.assertEqual(context["invoice_items"][1]["price_single"], self.item.price_str)
        self.assertEqual(context["invoice_items"][1]["discount"], self.item.discount_str)
        self.assertEqual(context["invoice_items"][1]["price_total"], self.item.total_str)

        # check miscellaneous
        self.assertFalse(context["show_page_number"])
        self.assertEqual("<svg>QR</svg>", context["qr_bill_svg"])

    def test_render_invoice_html_renders_template(self):
        """Test that render_invoice_html renders the invoice HTML template with context."""
        from sale.utils.invoice_pdf_generation import generate_html_invoice
        html = generate_html_invoice(self.context)
        hashed_result = hashlib.sha256(html.encode()).hexdigest()
        self.assertEqual("f359a8bdb72a7e54cc7c3ff7eddbb875a89e5ab49d288f47b76bf393dd872985", hashed_result)

    def test_generate_base_pdf_creates_pdf_and_page_count(self):
        """Test that generate_base_pdf returns PDF bytes and correct page count."""
        from sale.utils.invoice_pdf_generation import generate_pdf_from_html
        # Render a simple HTML for testing
        html = "<html><body><h1>Test PDF</h1><p>Page 1</p></body></html>"
        pdf_bytes, page_count = generate_pdf_from_html(html, "/")
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 100)  # Should be a non-trivial PDF
        self.assertEqual(page_count, 1)

    def test_create_page_number_overlay_creates_overlay(self):
        """Test that create_page_number_overlay returns a BytesIO PDF with the correct page number text."""
        from sale.utils.invoice_pdf_generation import create_page_number_overlay
        from PyPDF2 import PdfReader
        overlay_stream = create_page_number_overlay(0, 3)
        self.assertIsNotNone(overlay_stream)
        self.assertTrue(hasattr(overlay_stream, 'read'))
        overlay_stream.seek(0)
        reader = PdfReader(overlay_stream)
        self.assertEqual(len(reader.pages), 1)
        # Optionally, check that the PDF contains the expected text (requires text extraction)
        page = reader.pages[0]
        text = page.extract_text()
        self.assertIn("Seite 1 von 3", text)

    def test_add_page_numbers_to_pdf_adds_numbers(self):
        """Test that add_page_numbers_to_pdf adds page numbers to each page of a PDF."""
        from sale.utils.invoice_pdf_generation import generate_pdf_from_html, add_page_numbers_to_pdf
        from PyPDF2 import PdfReader
        # Create a multipage PDF
        html = """
        <html><body>
        <h1>Test PDF</h1>
        <div style='page-break-after: always;'></div>
        <h1>Page 2</h1>
        </body></html>
        """
        pdf_bytes, page_count = generate_pdf_from_html(html, "/")
        self.assertEqual(page_count, 2)
        # Add page numbers
        numbered_pdf_stream = add_page_numbers_to_pdf(pdf_bytes, page_count)
        self.assertIsNotNone(numbered_pdf_stream)
        numbered_pdf_stream.seek(0)
        reader = PdfReader(numbered_pdf_stream)
        self.assertEqual(len(reader.pages), 2)
        # Check that both pages contain the correct page number text
        text1 = reader.pages[0].extract_text()
        text2 = reader.pages[1].extract_text()
        self.assertIn("Seite 1 von 2", text1)
        self.assertIn("Seite 2 von 2", text2)

    def test_create_pdf_content_returns_pdf_content(self):
        """Test that create_pdf_content returns a PDFContent object with correct content and filename."""
        from sale.utils.invoice_pdf_generation import create_pdf_content, PDFContent
        # Create a dummy BytesIO PDF stream
        from io import BytesIO
        dummy_pdf_bytes = b"%PDF-1.4 dummy pdf content"
        pdf_stream = BytesIO(dummy_pdf_bytes)
        invoice_id = "INV-2024-001"
        pdf_content = create_pdf_content(pdf_stream, invoice_id)
        self.assertIsInstance(pdf_content, PDFContent)
        self.assertEqual(pdf_content.content, dummy_pdf_bytes)
        self.assertEqual(pdf_content.filename, f"invoice_{invoice_id}_numbered.pdf")
        self.assertEqual(pdf_content.mime_type, "application/pdf")

    def test_generate_qr_code_html_contains_quoted_svg(self):
        """Test that generate_qr_code_html returns HTML containing the quoted SVG content."""
        from sale.utils.invoice_pdf_generation import generate_html_qr_page
        from urllib.parse import quote
        svg_content = '<svg><rect width="100" height="100" style="fill:rgb(0,0,0);"/></svg>'
        context = self.context.copy()
        context["qr_bill_svg"] = svg_content
        html = generate_html_qr_page(svg_content, context)


        self.assertIsInstance(html, str)
        self.assertIn(quote(svg_content), html)

