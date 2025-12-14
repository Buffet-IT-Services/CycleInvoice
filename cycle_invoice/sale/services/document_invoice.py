"""Service for document invoice."""
from django.contrib.auth import get_user_model
from django.db import transaction

from cycle_invoice.common.services import model_update
from cycle_invoice.contact.selectors.customer import customer_get
from cycle_invoice.sale.models import Invoice


@transaction.atomic
def document_invoice_create(*, invoice_number: str, customer: int, date: str, due_date: str, header_text: str = "",
                            footer_text: str = "", user: get_user_model) -> Invoice:
    """Create a new document invoice."""
    document_invoice = Invoice(
        invoice_number=invoice_number,
        customer_id=customer,
        date=date,
        due_date=due_date,
        header_text=header_text,
        footer_text=footer_text
    )
    document_invoice.save(user=user)
    return document_invoice


@transaction.atomic
def document_invoice_update(*, invoice: Invoice, data: dict, user: get_user_model) -> Invoice:
    """Update an existing document invoice."""
    non_side_effect_fields: list[str] = [
        "invoice_number",
        "customer",
        "date",
        "due_date",
        "header_text",
        "footer_text"
    ]

    # If 'customer' is provided as an ID, convert it to a Customer object
    if "customer" in data and isinstance(data["customer"], int):
        data["customer"] = customer_get(data["customer"])

    return model_update(instance=invoice, fields=non_side_effect_fields, data=data, user=user)[0]
