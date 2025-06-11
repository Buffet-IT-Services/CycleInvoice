"""
Views for the sale application.

This module contains view functions for handling sale-related requests,
including invoice generation and PDF rendering.
"""

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpRequest, HttpResponse

from sale.utils import generate_invoice_pdf_two_pass


def generate_invoice_pdf(request: HttpRequest, invoice_id: int) -> HttpResponse:
    """
    Generate an invoice PDF.

    :param invoice_id: The ID of the invoice to generate.
    :param request: The HTTP request object.
    :return:
    """
    invoice_pdf = generate_invoice_pdf_two_pass(request, invoice_id)

    pdf_content = invoice_pdf.content

    file_path = f"invoice_{invoice_id}.pdf"
    default_storage.save(file_path, ContentFile(pdf_content))



    print(default_storage.url(file_path))
    print(default_storage.generate_filename(file_path))

    response = HttpResponse(content_type="application/pdf")

    # To display PDF in the browser instead of downloading it, use 'inline' instead of 'attachment'
    # This will make the browser render the PDF directly
    response["Content-Disposition"] = 'inline; filename="invoice_test.pdf"'

    # Set Content-Type to application/pdf
    response["Content-Type"] = "application/pdf"

    response["Content-Length"] = len(invoice_pdf.content)
    response.write(invoice_pdf.content)
    return response
