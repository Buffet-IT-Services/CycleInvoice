"""URL configuration for the sale app."""
from django.urls import path

from sale.api.document_invoice import InvoiceCreateApi, InvoiceDetailApi, InvoiceListApi

urlpatterns = [
    path("", InvoiceListApi.as_view(), name="document-invoice-list"),
    path("<int:pk>/", InvoiceDetailApi.as_view(), name="document-invoice-detail"),
    path("create/", InvoiceCreateApi.as_view(), name="document-invoice-create"),
]
