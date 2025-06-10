"""
PDF generation utilities for invoices.

This module provides functions for generating PDF invoices with page numbers,
QR codes, and other features required for Swiss invoicing standards.
"""
import os
from dataclasses import dataclass
from io import BytesIO
from typing import Any
from urllib.parse import quote

from PyPDF2 import PdfReader, PdfWriter
from django.http import HttpRequest
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from weasyprint import HTML

from sale.utils.swiss_qr import generate_swiss_qr





def prepare_invoice_context(invoice_id: int) -> dict[str, Any]:
    """
    Prepare the context data for invoice rendering.

    Returns:
        dict: The prepared context data with QR code

    """
    from sale.models import DocumentInvoice
    invoice = DocumentInvoice.objects.get(pk=invoice_id)

    context_data = {
        "company_info": {
            "company_name": os.getenv("COMPANY_NAME"),
            "company_address": os.getenv("COMPANY_ADDRESS"),
            "company_registration_id": os.getenv("COMPANY_REGISTRATION_ID"),
            "company_email": os.getenv("COMPANY_EMAIL"),
            "company_phone": os.getenv("COMPANY_PHONE"),
            "company_website": os.getenv("COMPANY_WEBSITE"),
            "zip": os.getenv("COMPANY_ZIP"),
            "city": os.getenv("COMPANY_CITY"),
            "country": os.getenv("COMPANY_COUNTRY"),
            "company_bank_account": os.getenv("COMPANY_BANK_ACCOUNT"),
        },
        "invoice_details": {
            "total_sum": invoice.total_sum,
            "invoice_number": invoice.invoice_number,
            "invoice_primary_key": invoice_id,
            "created_date": invoice.date.strftime("%d.%m.%Y"),
            "due_date": invoice.due_date.strftime("%d.%m.%Y"),
            "header_text": invoice.header_text,
            "footer_text": invoice.footer_text,
        },
        "customer": {
            "name": invoice.customer.__str__(),
            "street": f"{invoice.customer.address.street} {invoice.customer.address.number}",
            "postal_code": invoice.customer.address.zip_code,
            "city": invoice.customer.address.city,
            "country": invoice.customer.address.country,
            "address_block": invoice.customer.address_block,
        },
        "show_page_number": False}

    # Generate the QR bill and add it to the context
    generate_swiss_qr(context_data, context_data["invoice_details"]["total_sum"])

    return context_data


def render_invoice_html(
        context_data: dict[str, Any], template_name: str = "sale/invoice.html"
) -> str:
    """
    Render the invoice HTML template with the given context.

    Args:
        context_data (dict): The context data for rendering
        template_name (str): The name of the template to render

    Returns:
        str: The rendered HTML

    """
    return render_to_string(template_name, context_data)


def generate_base_pdf(
        html_content: str, base_url: str | None = None
) -> tuple[bytes, int]:
    """
    Generate a PDF from HTML content using WeasyPrint.

    Args:
        html_content (str): The HTML content to convert to PDF
        base_url (str, optional): The base URL for resolving relative URLs

    Returns:
        tuple: (PDF bytes, total page count)

    """
    document = HTML(string=html_content, base_url=base_url, encoding="utf-8").render()
    total_pages = len(document.pages)
    pdf_file = document.write_pdf()

    return pdf_file, total_pages


def create_page_number_overlay(page_num: int, total_pages: int) -> BytesIO:
    """
    Create a PDF overlay with page numbers.

    Args:
        page_num (int): The current page number (0-based)
        total_pages (int): The total number of pages

    Returns:
        BytesIO: A BytesIO object containing the page number overlay PDF

    """
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    # Draw the page number (positioned to overlap with footer)
    can.setFont("Helvetica", 22)  # Smaller font size
    can.setFillColorRGB(1, 1, 1)  # White color
    text = f"Seite {page_num + 1} von {total_pages}"

    # Position in the bottom right area of the footer
    can.drawRightString(530, 20, text)
    can.save()

    # Move to the beginning of the BytesIO buffer
    packet.seek(0)

    return packet


def add_page_numbers_to_pdf(pdf_data: bytes, total_pages: int) -> BytesIO:
    """
    Add page numbers to each page of a PDF.

    Args:
        pdf_data (bytes): The original PDF data
        total_pages (int): The total number of pages

    Returns:
        BytesIO: A BytesIO object containing the PDF with page numbers

    """
    input_pdf = PdfReader(BytesIO(pdf_data))
    output_pdf = PdfWriter()

    # For each page, add page number
    for page_num in range(total_pages):
        # Get the page from the original PDF
        page = input_pdf.pages[page_num]

        # Create the page number overlay
        packet = create_page_number_overlay(page_num, total_pages)

        # Create a new PDF with the page number
        new_pdf = PdfReader(packet)

        # Merge the original page with the page number
        page.merge_page(new_pdf.pages[0])

        # Add the page to the output PDF
        output_pdf.add_page(page)

    # Write the output PDF to BytesIO
    output_stream = BytesIO()
    output_pdf.write(output_stream)
    output_stream.seek(0)

    return output_stream


@dataclass
class PDFContent:
    """Class for storing PDF content and metadata."""

    content: bytes
    filename: str
    mime_type: str = "application/pdf"


def create_pdf_content(pdf_stream: BytesIO, invoice_id: str) -> PDFContent:
    """
    Create a PDFContent object with the PDF content.

    Args:
        pdf_stream (BytesIO): The PDF content as a BytesIO stream
        invoice_id (str): The invoice ID for the filename

    Returns:
        PDFContent: Object containing PDF content and metadata

    """
    filename = f"invoice_{invoice_id}_numbered.pdf"

    # Get the bytes from the BytesIO stream
    pdf_stream.seek(0)
    content = pdf_stream.getvalue()

    return PDFContent(content=content, filename=filename)


def generate_qr_code_pdf(
        svg_content: str, context_data: dict[str, Any], request: HttpRequest
) -> PdfReader:
    """
    Generate a PDF containing only the QR code.

    Args:
        svg_content (str): The SVG content of the QR code
        context_data (dict): The context data for the HTML Render
        request: The HTTP request object for building absolute URLs

    Returns:
        PdfReader: A PdfReader object containing the QR code PDF

    """
    # Create HTML for the QR code page
    svg_content = quote(svg_content)
    qr_html = render_to_string(
        "sale/qr_code.html", {**context_data, "svg_content": svg_content}
    )

    # Generate PDF from the HTML string directly using WeasyPrint
    qr_document = HTML(
        string=qr_html, base_url=request.build_absolute_uri("/"), encoding="utf-8"
    ).render()
    qr_pdf_bytes = qr_document.write_pdf()

    # Create a PDF reader for the QR page
    return PdfReader(BytesIO(qr_pdf_bytes))


def generate_invoice_pdf_two_pass(
        request: HttpRequest, invoice_id: int) -> "PDFContent":
    """
    Generate a PDF invoice using WeasyPrint with manual page numbering.

    Args:
        request: The HTTP request object
        invoice_id (int): The ID of the invoice to generate

    Returns:
        PDFContent: Object containing PDF content and metadata

    """
    # Step 1: Prepare the context data
    context_data = prepare_invoice_context(invoice_id)

    # Step 2: Render the HTML
    html_content = render_invoice_html(context_data)

    # Step 3: Generate the base PDF and get page count
    pdf_data, total_pages = generate_base_pdf(
        html_content, request.build_absolute_uri("/")
    )
    # Total pages detected: {total_pages}

    # Step 4: Add page numbers to the PDF
    pdf_with_page_numbers = add_page_numbers_to_pdf(pdf_data, total_pages)

    # Step 5: Generate QR code PDF and combine with invoice PDF
    final_output = PdfWriter()

    # Add all pages from the invoice PDF with page numbers
    numbered_pdf = PdfReader(pdf_with_page_numbers)
    for page in numbered_pdf.pages:
        final_output.add_page(page)

    # Generate and add the QR code page
    qr_pdf = generate_qr_code_pdf(
        context_data["qr_bill_svg"], context_data, request
    )
    final_output.add_page(qr_pdf.pages[0])

    # Write the final PDF to a BytesIO stream
    final_stream = BytesIO()
    final_output.write(final_stream)
    final_stream.seek(0)

    # Create and return the PDF content
    return create_pdf_content(
        final_stream, context_data["invoice_details"]["invoice_number"]
    )
