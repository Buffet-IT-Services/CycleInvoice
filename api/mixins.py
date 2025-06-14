from typing import TYPE_CHECKING, Sequence, Type

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated, DjangoModelPermissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


def get_auth_header(headers) -> tuple[str, str] | None:
    """Extracts the Authorization header from the request headers."""
    value = headers.get("Authorization")

    if not value:
        return None

    auth_type, auth_value = value.split()[:2]

    return auth_type, auth_value


if TYPE_CHECKING:
    # This is going to be resolved in the stub library
    # https://github.com/typeddjango/djangorestframework-stubs/
    from rest_framework.permissions import _PermissionClass

    PermissionClassesType = Sequence[_PermissionClass]
else:
    PermissionClassesType = Sequence[Type[BasePermission]]


class ApiAuthMixin:
    """Mixin to provide authentication and permission classes for API views."""
    authentication_classes: Sequence[Type[BaseAuthentication]] = (JSONWebTokenAuthentication,)
    permission_classes: PermissionClassesType = (IsAuthenticated, DjangoModelPermissions,)
