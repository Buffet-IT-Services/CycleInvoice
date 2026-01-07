"""Tests for Django settings configuration."""
import importlib
import os
import sys

from django.test import TestCase


class HealthCheckAppsConfigTest(TestCase):
    """Tests for conditional health check apps configuration."""

    def setUp(self) -> None:
        """Set up the test environment."""
        # Store original values
        self.original_env = os.environ.copy()
        self.original_modules = sys.modules.copy()

    def tearDown(self) -> None:
        """Clean up the test environment."""
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_env)

        for key in sys.modules:
            if key not in self.original_modules:
                del sys.modules[key]

    def test_storage_health_check_excluded_when_s3_not_configured(self) -> None:
        """Test that health_check.storage is excluded when S3_BUCKET_NAME is not set."""
        # In the test environment, storage health check should always be excluded
        # because 'test' is in sys.argv
        from config.django import base  # noqa: PLC0415

        self.assertNotIn("health_check.storage", base.INSTALLED_APPS)

    def test_celery_health_check_excluded_when_broker_not_configured(self) -> None:
        """Test that celery health checks are excluded when CELERY_BROKER_URL is not set."""
        # Remove CELERY_BROKER_URL if it exists
        if "CELERY_BROKER_URL" in os.environ:
            del os.environ["CELERY_BROKER_URL"]

        # Reload the module to apply the change
        from config.django import base  # noqa: PLC0415
        importlib.reload(base)

        self.assertNotIn("health_check.contrib.celery", base.INSTALLED_APPS)
        self.assertNotIn("health_check.contrib.celery_ping", base.INSTALLED_APPS)

    def test_celery_health_check_included_when_broker_configured(self) -> None:
        """Test that celery health checks are included when CELERY_BROKER_URL is set."""
        # Set CELERY_BROKER_URL
        os.environ["CELERY_BROKER_URL"] = "redis://localhost:6379"

        # Reload the module to apply the change
        from config.django import base  # noqa: PLC0415
        importlib.reload(base)

        self.assertIn("health_check.contrib.celery", base.INSTALLED_APPS)
        self.assertIn("health_check.contrib.celery_ping", base.INSTALLED_APPS)

    def test_base_health_checks_always_included(self) -> None:
        """Test that base health check apps are always included."""
        from config.django import base  # noqa: PLC0415

        # These should always be present
        self.assertIn("health_check", base.INSTALLED_APPS)
        self.assertIn("health_check.db", base.INSTALLED_APPS)
        self.assertIn("health_check.cache", base.INSTALLED_APPS)
        self.assertIn("health_check.contrib.migrations", base.INSTALLED_APPS)
