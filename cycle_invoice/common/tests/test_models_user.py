"""Tests for the common model User."""

from django.test import TestCase

from cycle_invoice.common.tests.factories import UserFactory


class TestModelsUser(TestCase):
    """Tests for the common model User."""

    def test_user_str(self) -> None:
        """Test User.__str__()."""
        user = UserFactory.create()
        self.assertEqual(str(user), user.email)
