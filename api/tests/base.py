"""Provides Tokens for API tests."""

from django.test import Client


def token_admin_create(client: Client) -> str:
    """Create a superuser if not exists and return a JWT token for it."""
    from django.contrib.auth.models import User
    from django.urls import reverse

    user, created = User.objects.get_or_create(
        username="test-admin",
        defaults={
            "email": "test-admin@buffetitservices.ch",
            "is_superuser": True
        }
    )
    if created or not user.check_password("test-admin-password"):
        user.set_password("test-admin-password")
        user.save()
    url = reverse("jwt-token-obtain")
    resp = client.post(url, {"username": "test-admin", "password": "test-admin-password"}, format="json")
    return resp.json()["token"]


def token_user_create(client: Client, permissions: list[str] | None = None) -> str:
    """Create a user with specific permissions and return a JWT token for it."""
    from django.contrib.auth.models import Permission, User
    from django.urls import reverse

    user, created = User.objects.get_or_create(
        username="test-user",
        defaults={
            "email": "test-user@buffetitservices.ch",
        }
    )
    if created or not user.check_password("test-user-password"):
        user.set_password("test-user-password")
        user.save()

    user.user_permissions.clear()
    if permissions:
        for perm in permissions:
            permission = Permission.objects.get(codename=perm)
            user.user_permissions.add(permission)

    url = reverse("jwt-token-obtain")
    resp = client.post(url, {"username": "test-user", "password": "test-user-password"}, format="json")
    return resp.json()["token"]


def token_norights_create(client: Client) -> str:
    """Create a user with no rights if not exists and return a JWT token for it."""
    from django.contrib.auth.models import User
    from django.urls import reverse

    user, created = User.objects.get_or_create(
        username="test-norights",
        defaults={
            "email": "test-norights@buffetitservices.ch",
        }
    )
    if created or not user.check_password("test-norights-password"):
        user.set_password("test-norights-password")
        user.save()
    url = reverse("jwt-token-obtain")
    resp = client.post(url, {"username": "test-norights", "password": "test-norights-password"}, format="json")
    return resp.json()["token"]

