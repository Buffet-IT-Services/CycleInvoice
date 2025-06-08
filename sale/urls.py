from django.urls import path

from . import views

app_name = "sale"
urlpatterns = [
    path("generate/invoice/pdf/", views.generate_invoice_pdf, name="index")
]
