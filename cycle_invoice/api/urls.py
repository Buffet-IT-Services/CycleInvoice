"""URLs for the api app."""
from django.http import HttpRequest, JsonResponse
from django.urls import path
from django.views.decorators.http import require_safe
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


@require_safe
def healthcheck(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return a health check status for the API."""
    return JsonResponse({"status": "ok"}, status=200)


urlpatterns = [
    path("token/", obtain_jwt_token, name="jwt-token-obtain"),
    path("token/refresh/", refresh_jwt_token),
    path("healthcheck/", healthcheck, name="healthcheck"),
]
