"""URL configuration for the sale app."""
from django.urls import path

from sale.api.document_invoice import InvoiceListApi, InvoiceDetailApi, InvoiceCreateApi

urlpatterns = [
    path("", InvoiceListApi.as_view(), name="list"),
    path("<int:pk>/", InvoiceDetailApi.as_view(), name="detail"),
    path("create/", InvoiceCreateApi.as_view(), name="create"),
]
