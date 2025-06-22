"""URL configuration for the sale app."""
from django.urls import include, path

from cycle_invoice.sale.api.document_invoice import (
    InvoiceCreateApi,
    InvoiceDeleteApi,
    InvoiceDetailApi,
    InvoiceListApi,
    InvoiceUpdateApi,
)

invoice_patterns = [
    path("create/", InvoiceCreateApi.as_view(), name="document-invoice-create"),
    path("<str:invoice_uuid>/", InvoiceDetailApi.as_view(), name="document-invoice-detail"),
    path("<str:invoice_uuid>/update/", InvoiceUpdateApi.as_view(), name="document-invoice-update"),
    path("<str:invoice_uuid>/delete/", InvoiceDeleteApi.as_view(), name="document-invoice-delete"),
    path("", InvoiceListApi.as_view(), name="document-invoice-list"),
]

urlpatterns = [
    path("invoice/", include(invoice_patterns)),
]
