import json
import os

from django.conf import settings
from django.http.response import HttpResponse

from sale.utils import generate_invoice_pdf_two_pass


def generate_invoice_pdf(request):
    """
    Generate Invoice PDF
    :param request:
    :return: HttpResponse with PDF content
    """
    # Example Content Data from A Json File
    # TODO
    # Implement Your Invoice Fetching Logic with all the details if Line Items in invoice.

    json_file_path = os.path.join(settings.BASE_DIR, "example_data/invoice_data.json")
    with open(json_file_path) as file:
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
