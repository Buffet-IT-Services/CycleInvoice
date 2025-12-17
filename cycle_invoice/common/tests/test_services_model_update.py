"""Tests for the common service method model_update()."""

from django.test import TestCase

from cycle_invoice.common.selectors import get_system_user


class TestServicesModelUpdate(TestCase):
    """Tests for the common service method model_update()."""

    def