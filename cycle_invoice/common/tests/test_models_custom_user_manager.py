"""Unit tests for CustomUserManager behavior."""

from django.test import TestCase

from cycle_invoice.common.models import User
from cycle_invoice.common.tests.factories import UserFactory
from cycle_invoice.common.tests.faker import faker


class TestModelsCustomUserManager(TestCase):
    """Tests for the CustomUserManager attached to the User model."""

    def setUp(self) -> None:
        """Prepare bound manager and persisted user fixture."""
        self.manager = User.objects
        self.user = UserFactory.create(email="eMAil@email.local")

    def test_private_create_user(self) -> None:
        """_create_user returns an active user without a usable password."""
        user = self.manager._create_user(email="email@email.local")
        self.assertTrue(user.is_active)
        self.assertEqual("email@email.local", user.email)
        self.assertFalse(user.has_usable_password())

    def test_private_create_user_normalize_email(self) -> None:
        """_create_user normalizes the domain part of the email."""
        user = self.manager._create_user(email="eMaIl@eMAil.loCal")
        self.assertEqual("eMaIl@email.local", user.email)

    def test_create_user(self) -> None:
        """create_user creates a non-staff, non-superuser without a password."""
        user = self.manager.create_user(email="email@email.local")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.has_usable_password())

    def test_create_user_with_password(self) -> None:
        """create_user with a password sets a usable password."""
        password = faker.password()
        user = self.manager.create_user(email="email@email.local", password=password)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self) -> None:
        """create_superuser marks user as staff and superuser without a password."""
        user = self.manager.create_superuser(email="email@email.local")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertFalse(user.has_usable_password())

    def test_create_superuser_with_password(self) -> None:
        """create_superuser with password sets it correctly."""
        password = faker.password()
        user = self.manager.create_superuser(email="email@email.local", password=password)
        self.assertTrue(user.check_password(password))

    def test_get_by_natural_key(self) -> None:
        """get_by_natural_key finds user using normalized email."""
        self.assertEqual(self.user, self.manager.get_by_natural_key("eMAil@email.local"))

    def test_get_by_natural_key_normalized(self) -> None:
        """get_by_natural_key normalizes input before lookup."""
        self.assertEqual(self.user, self.manager.get_by_natural_key("eMAil@emAIL.loCal"))
