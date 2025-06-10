"""
Views for the sale application.

This module contains view functions for handling sale-related requests,
including invoice generation and PDF rendering.
"""
import json
from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from sale.utils import generate_invoice_pdf_two_pass


def generate_invoice_pdf(request: HttpRequest) -> HttpResponse:
    """
    Generate an invoice PDF.

    :param request:
    :return:
    """
    json_file_path = Path(settings.BASE_DIR) / "example_data/invoice_data.json"
    with json_file_path.open() as file:
        context_data = json.load(file)

    generate_invoice_pdf = generate_invoice_pdf_two_pass(request, context_data)
    response = HttpResponse(content_type="application/pdf")

    # To display PDF in the browser instead of downloading it, use 'inline' instead of 'attachment'
    # This will make the browser render the PDF directly
    response["Content-Disposition"] = f'inline; filename="invoice2_{context_data["invoice_details"]["invoice_id"]}.pdf"'

    # Set Content-Type to application/pdf
    response["Content-Type"] = "application/pdf"

    response["Content-Length"] = len(generate_invoice_pdf.content)
    response.write(generate_invoice_pdf.content)
    return response
