"""Tests for the common selector method get_system_user()."""

from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user


class TestSelectorsGetSystemUser(TestCase):
    """Tests for selector method get_system_user()."""

    def test_get_system_user_values(self) -> None:
        """Test get_system_user()"""

        user = get_system_user()
        self.assertEqual(user.email, "system@cycleinvoice.local")
        self.assertEqual(user.first_name, "System")
        self.assertEqual(user.last_name, "User")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_get_system_user_idempotence(self) -> None:
        """Test get_system_user() idempotence"""

        user1 = get_system_user()
        user2 = get_system_user()
        self.assertEqual(user1, user2)
