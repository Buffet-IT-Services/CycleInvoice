"""URLs for the api app."""
from django.http import HttpRequest, JsonResponse
from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


def healthcheck(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return a health check status for the API."""
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("token/", obtain_jwt_token, name="jwt-token-obtain"),
    path("token/refresh/", refresh_jwt_token),
    path("sale/", include("cycle_invoice.sale.urls")),
    path("healthcheck/", healthcheck, name="healthcheck"),
]
