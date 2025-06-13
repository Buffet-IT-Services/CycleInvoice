"""URL configuration for the api app."""
from django.urls import include, path

urlpatterns = [
    path("invoice/", include("sale.urls")),
]
