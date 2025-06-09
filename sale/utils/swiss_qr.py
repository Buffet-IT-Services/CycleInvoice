from decimal import Decimal
from io import StringIO

from qrbill import QRBill


def generate_swiss_qr(context_data, invoice_amount):
    # Format the creditor address properly
    company_name = context_data["company_info"]["company_name"]
    company_address = context_data["company_info"]["company_address"]
    company_postal_code = context_data["company_info"].get(
        "company_postal_code", "8001"
    )
    company_city = context_data["company_info"].get("company_city", "Zürich")
    company_country = context_data["company_info"].get("company_country", "CH")

    # Format the debtor address properly
    customer_name = context_data["customer_info"]["to_address"]["name"]
    customer_street = context_data["customer_info"]["to_address"]["street"]
    customer_postal_code = context_data["customer_info"]["to_address"].get(
        "postal_code", ""
    )
    customer_city = context_data["customer_info"]["to_address"].get("city", "")
    customer_country = context_data["customer_info"]["to_address"].get("country", "CH")

    # Format the invoice amount to 2 decimal places
    formatted_amount =  Decimal(invoice_amount).quantize(Decimal("0.00")) if invoice_amount else 0

    # Generate a reference number based on the invoice ID if not available
    invoice_id = context_data["invoice_details"]["invoice_id"]
    reference_number = context_data.get("invoice_details", {}).get("reference_number")
    company_account_number = context_data.get("company_info", {}).get("company_bank_account")

    qr_bill = QRBill(
        account=company_account_number,  # Use a valid IBAN format
        creditor={
            "name": company_name,
            "line1": company_address,
            "line2": f"{company_postal_code} {company_city}",
            "country": company_country,
        },
        debtor={
            "name": customer_name,
            "line1": customer_street,
            "line2": f"{customer_postal_code} {customer_city}",
            "country": customer_country,
        },
        amount=formatted_amount,
        currency="CHF"
    )

    # Generate QR bill as SVG string
    svg_buffer = StringIO()
    qr_bill.as_svg(svg_buffer)
    svg_content = svg_buffer.getvalue()

    # Modify the SVG to set width from 210mm to 180mm
    svg_content = svg_content.replace('width="210mm"', 'width="180mm"')
    svg_content = svg_content.replace('height="106mm"', 'height="90mm"')

    # Add the SVG content to the context data
    context_data["qr_bill_svg"] = svg_content

    # Also add QR bill data to context for potential use in the template
    context_data["qr_bill_data"] = {
        "account":  company_account_number,
        "reference": reference_number,
        "amount": formatted_amount,
        "currency": "CHF",
        "invoice_id": invoice_id,
    }

    return context_data
