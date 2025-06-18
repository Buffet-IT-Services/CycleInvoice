"""URL configuration for the sale app."""
from django.urls import include, path

from cycle_invoice.sale.api.document_invoice import InvoiceCreateApi, InvoiceDetailApi, InvoiceListApi, InvoiceUpdateApi

invoice_patterns = [
    path("", InvoiceListApi.as_view(), name="document-invoice-list"),
    path("<int:pk>/", InvoiceDetailApi.as_view(), name="document-invoice-detail"),
    path("create/", InvoiceCreateApi.as_view(), name="document-invoice-create"),
    path("<int:pk>/update/", InvoiceUpdateApi.as_view(), name="document-invoice-update"),
]

urlpatterns = [
    path("invoice/", include(invoice_patterns)),
]
