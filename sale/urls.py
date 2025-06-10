"""
URL configuration for the sale application.

This module contains URL patterns for the sale application, including
routes for invoice generation and other sale-related functionality.
"""
from django.urls import path

from . import views

app_name = "sale"
urlpatterns = [
    path("generate/invoice/pdf/", views.generate_invoice_pdf, name="index")
]
