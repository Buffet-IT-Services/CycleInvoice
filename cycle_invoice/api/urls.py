"""URL configuration for the api app."""
from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path("token/", obtain_jwt_token, name="jwt-token-obtain"),
    path("token/refresh/", refresh_jwt_token),
    path("sale/", include("cycle_invoice.sale.urls")),
]
