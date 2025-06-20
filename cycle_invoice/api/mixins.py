"""Mixins for the api app."""
import copy
from collections.abc import Sequence

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.permissions import DjangoModelPermissions as BaseDjangoModelPermissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


def get_auth_header(headers: dict) -> tuple[str, str] | None:
    """Extract the Authorization header from the request headers."""
    value = headers.get("Authorization")

    if not value:
        return None

    auth_type, auth_value = value.split()[:2]

    return auth_type, auth_value


class DjangoModelPermissions(BaseDjangoModelPermissions):
    """Custom DjangoModelPermissions to include view permissions for GET requests."""

    def __init__(self) -> None:
        """Initialize DjangoModelPermissions with custom permissions."""
        self.perms_map = copy.deepcopy(self.perms_map)  # from EunChong's answer
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]


class ApiAuthMixin:
    """Mixin to provide authentication and permission classes for API views."""

    authentication_classes: Sequence[type[BaseAuthentication]] = (JSONWebTokenAuthentication,)
    permission_classes: Sequence[type[BasePermission]] = (IsAuthenticated, DjangoModelPermissions)
