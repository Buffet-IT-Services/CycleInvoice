"""URL configuration for the sale app."""
from django.urls import path

from sale.api import InvoiceListApi

urlpatterns = [
    path("", InvoiceListApi.as_view(), name="invoice-list"),
]
