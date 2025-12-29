"""Tests for the urls file of the api app."""
from django.test import TestCase


class UrlsTest(TestCase):
    """Tests for the urls file."""

    def test_healthcheck(self) -> None:
        """Test the health check endpoint."""
        response = self.client.get("/healthcheck/")
        self.assertEqual(response.status_code, 200)
