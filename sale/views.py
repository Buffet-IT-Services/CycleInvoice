"""
Views for the sale application.

This module contains view functions for handling sale-related requests,
including invoice generation and PDF rendering.
"""

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
    response = HttpResponse(content_type="application/pdf")

    # To display PDF in the browser instead of downloading it, use 'inline' instead of 'attachment'
    # This will make the browser render the PDF directly
    response["Content-Disposition"] = f'inline; filename="invoice_test.pdf"'

    # Set Content-Type to application/pdf
    response["Content-Type"] = "application/pdf"

    response["Content-Length"] = len(invoice_pdf.content)
    response.write(invoice_pdf.content)
    return response

