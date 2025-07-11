"""
Swiss QR bill generation utilities.

This module provides functionality for generating Swiss QR bills
compliant with the Swiss payment standards.
"""
from decimal import Decimal
from io import StringIO
from typing import Any

from qrbill import QRBill


def generate_swiss_qr(context_data: dict[str, Any]) -> dict[str, Any]:
    """
    Generate a Swiss QR bill and add it to the context data.

    Args:
        context_data: Dictionary containing invoice and company information
    Returns:
        Updated context data with QR bill information

    """
    # Format the invoice amount to 2 decimal places
    formatted_amount = Decimal(context_data["invoice_details"]["total_sum"]).quantize(Decimal("0.00"))

    qr_bill = QRBill(
        account=context_data["company_info"]["company_bank_account"],
        creditor={
            "name": context_data["company_info"]["company_name"],
            "line1": context_data["company_info"]["company_address"],
            "line2": f"{context_data["company_info"]["zip"]} {context_data["company_info"]["city"]}",
            "country": context_data["company_info"]["country"],
        }, debtor={
            "name": context_data["customer"]["name"],
            "line1": context_data["customer"]["street"],
            "line2": f"{context_data["customer"]["postal_code"]} {context_data["customer"]["city"]}",
            "country": context_data["customer"]["country"],
        }, amount=formatted_amount,
        language="de",
        additional_information=f"Rechnung {context_data["invoice_details"]["invoice_number"]}",
        reference_number=generate_qr_reference(context_data["invoice_details"]["invoice_primary_key"]),
    )

    # Generate QR bill as SVG string
    svg_buffer = StringIO()
    qr_bill.as_svg(svg_buffer)
    svg_content = svg_buffer.getvalue()

    # Add the SVG content to the context data
    context_data["qr_bill_svg"] = svg_content

    return context_data


def modulo10_recursive(number: str) -> str:
    """
    Calculate the check digit using the recursive Modulo 10 algorithm (Swiss QR standard, Annex B).

    Args:
        number: A string of digits (up to 26 characters) for which the check digit is calculated.
    Returns the check digit as a string.

    """
    table = [0, 9, 4, 6, 8, 2, 7, 1, 3, 5]
    carry = 0
    for digit in number:
        carry = table[(int(digit) + carry) % 10]
    check_digit = (10 - carry) % 10
    return str(check_digit)


def generate_qr_reference(base_number: str) -> str:
    """
    Generate a QR reference number according to the Swiss QR standard.

    - 26 numeric characters (padded with leading zeros)
    - Check digit using recursive Modulo 10 (Annex B)
    """
    base = str(base_number).zfill(26)
    check_digit = modulo10_recursive(base)
    return base + check_digit
