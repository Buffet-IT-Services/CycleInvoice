"""Service for document invoice."""
from typing import List

from django.db import transaction

from common.services import model_update
from sale.models import DocumentInvoice


@transaction.atomic
def document_invoice_create(*, invoice_number: str, customer: int, date: str, due_date: str, header_text: str = "",
                            footer_text: str = "") -> DocumentInvoice:
    """Create a new document invoice."""
    invoice = DocumentInvoice.objects.create(
        invoice_number=invoice_number,
        customer_id=customer,
        date=date,
        due_date=due_date,
        header_text=header_text,
        footer_text=footer_text
    )
    return invoice


@transaction.atomic
def document_invoice_update(*, invoice: DocumentInvoice, data: dict) -> DocumentInvoice:
    """Update an existing document invoice."""
    non_side_effect_fields: List[str] = [
        "invoice_number",
        "customer",
        "date",
        "due_date",
        "header_text",
        "footer_text"
    ]

    invoice, has_updates = model_update(instance=invoice, fields=non_side_effect_fields, data=data)

    return invoice
