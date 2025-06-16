"""Tests for API mixins."""
from django.test import TestCase
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.mixins import ApiAuthMixin, DjangoModelPermissions, get_auth_header


class MixinsTest(TestCase):
    """Tests for API mixins."""

    def test_get_auth_header_valid(self) -> None:
        """Test that get_auth_header correctly extracts the auth type and value."""
        headers = {"Authorization": "Bearer sometoken"}
        result = get_auth_header(headers)
        self.assertEqual(result[0], "Bearer")
        self.assertEqual(result[1], "sometoken")

    def test_get_auth_header_missing(self) -> None:
        """Test that get_auth_header returns None when Authorization header is missing."""
        headers = {}
        result = get_auth_header(headers)
        self.assertIsNone(result)

    def test_get_auth_header_invalid_format(self) -> None:
        """Test that get_auth_header raises ValueError for invalid Authorization header format."""
        headers = {"Authorization": "Bearer"}
        self.assertRaises(ValueError, get_auth_header, headers)


class DjangoModelPermissionsTest(TestCase):
    """Tests for DjangoModelPermissions."""

    def test_django_model_permissions_get(self) -> None:
        """Test that DjangoModelPermissions includes view permissions for GET requests."""
        perms = DjangoModelPermissions()
        self.assertIn("GET", perms.perms_map)
        self.assertIn("%(app_label)s.view_%(model_name)s", perms.perms_map["GET"])


class ApiAuthMixinTest(TestCase):
    """Tests for ApiAuthMixin."""

    def test_api_auth_mixin_classes(self) -> None:
        """Test that ApiAuthMixin has the correct authentication and permission classes."""
        self.assertIn(JSONWebTokenAuthentication, ApiAuthMixin.authentication_classes)
        self.assertEqual(1, len(ApiAuthMixin.authentication_classes))
        self.assertIn(IsAuthenticated, ApiAuthMixin.permission_classes)
        self.assertIn(DjangoModelPermissions, ApiAuthMixin.permission_classes)
        self.assertEqual(2, len(ApiAuthMixin.permission_classes))
