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

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpRequest
from django.template.loader import render_to_string
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from weasyprint import HTML

from cycle_invoice.sale.models import DocumentItem, Invoice
from cycle_invoice.sale.utils.swiss_qr import generate_swiss_qr


@dataclass
class PDFContent:
    """Class for storing PDF content and metadata."""

    content: bytes
    filename: str
    mime_type: str = "application/pdf"

def generate_content(invoice_id: int) -> dict[str, Any]:
    """
    Prepare the context data for invoice rendering.

    Returns:
        dict: The dictionary containing all necessary data for rendering the invoice

    """
    invoice = Invoice.objects.get(pk=invoice_id)

    document_items = DocumentItem.objects.filter(document=invoice)
    invoice_items = [
        {
            "product_name": item.title,
            "product_description": item.description,
            "quantity": item.quantity_str,
            "price_single": item.price_str,
            "discount": item.discount_str,
            "price_total": item.total_str,
        }
        for item in document_items
    ]

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
            "total_sum": invoice.total_sum.__str__(),
            "invoice_number": invoice.document_number,
            "invoice_primary_key": invoice_id,
            "created_date": invoice.date.strftime("%d.%m.%Y"),
            "due_date": invoice.due_date.strftime("%d.%m.%Y"),
            "header_text": invoice.header_text,
            "footer_text": invoice.footer_text,
        },
        "customer": {
            "name": invoice.party.__str__(),
            "street": f"{invoice.party.address.street} {invoice.party.address.number}",
            "postal_code": invoice.party.address.zip_code,
            "city": invoice.party.address.city,
            "country": invoice.party.address.country,
            "address_block": invoice.party.address_block,
        },
        "show_page_number": False,
        "invoice_items": invoice_items
    }

    # Generate the QR bill and add it to the context
    generate_swiss_qr(context_data)

    return context_data


def generate_html_invoice(context_data: dict[str, Any]) -> str:
    """
    Generate the HTML content for the invoice using the provided context data.

    Args:
        context_data (dict): The context data for rendering

    Returns:
        str: The rendered HTML

    """
    return render_to_string("sale/invoice.html", context_data)


def generate_html_qr_page(context_data: dict[str, Any]) -> str:
    """
    Generate the HTML content for the qr page using the provided context data.

    Args:
        context_data (dict): The context data for rendering

    Returns:
        str: The rendered HTML

    """
    svg_content = quote(context_data["qr_bill_svg"])
    return render_to_string("sale/qr_code.html", {**context_data, "svg_content": svg_content})


def generate_pdf_from_html(html_content: str, base_url: str) -> bytes:
    """
    Generate a PDF from HTML content using WeasyPrint.

    Args:
        html_content (str): The HTML content to convert to PDF
        base_url (str, optional): The base URL for resolving relative URLs

    Returns:
        bytes: The generated PDF as bytes

    """
    document = HTML(string=html_content, base_url=base_url, encoding="utf-8").render()
    return document.write_pdf()


def add_page_numbers_to_pdf(pdf_data: bytes) -> BytesIO:
    """
    Add page numbers to each page of a PDF.

    Args:
        pdf_data (bytes): The original PDF data

    Returns:
        BytesIO: A BytesIO object containing the PDF with page numbers

    """
    input_pdf = PdfReader(BytesIO(pdf_data))
    output_pdf = PdfWriter()

    for page_num, page in enumerate(input_pdf.pages, start=1):
        # Create overlay with page number
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.setFont("Helvetica", 22)
        can.setFillColorRGB(1, 1, 1)
        can.drawRightString(530, 20, f"Seite {page_num} von {len(input_pdf.pages)}")
        can.save()
        packet.seek(0)

        # Merge overlay with the current page
        overlay_pdf = PdfReader(packet)
        page.merge_page(overlay_pdf.pages[0])
        output_pdf.add_page(page)

    # Write the final PDF to a BytesIO stream
    output_stream = BytesIO()
    output_pdf.write(output_stream)
    output_stream.seek(0)
    return output_stream

def add_pdf_to_storage(invoice_pdf: PDFContent) -> None:
    """
    Save the generated PDF invoice to the default storage.

    :param invoice_pdf: PDFContent object containing the PDF data and filename
    """
    pdf_content = invoice_pdf.content

    default_storage.save(invoice_pdf.filename, ContentFile(pdf_content))


def generate_invoice_pdf(request: HttpRequest, invoice_id: int) -> None:
    """
    Generate a PDF invoice using WeasyPrint with manual page numbering.

    Args:
        request: The HTTP request object
        invoice_id (int): The ID of the invoice to generate

    Returns:
        PDFContent: Object containing PDF content and metadata

    """
    # Prepare the content including qr code for the invoice
    content = generate_content(invoice_id)

    # Render the HTML content
    html_invoice = generate_html_invoice(content)
    html_qr_page = generate_html_qr_page(content)

    # Generate the PDF from the HTML content
    pdf_data_invoice = generate_pdf_from_html(html_invoice, request.build_absolute_uri("/"))
    pdf_data_qr_page = generate_pdf_from_html(html_qr_page, request.build_absolute_uri("/"))

    # Add Page numbers to the PDF
    pdf_data_invoice = add_page_numbers_to_pdf(pdf_data_invoice)

    # Build the final PDF by merging the invoice and QR code pages
    output_pdf = PdfWriter()
    for page in PdfReader(pdf_data_invoice).pages:
        output_pdf.add_page(page)
    output_pdf.add_page(PdfReader(BytesIO(pdf_data_qr_page)).pages[0])

    # Write the final PDF to a BytesIO stream
    final_stream = BytesIO()
    output_pdf.write(final_stream)
    final_stream.seek(0)

    # Create and return the PDF content
    add_pdf_to_storage(PDFContent(final_stream.getvalue(), f"invoice_{invoice_id}.pdf"))
