"""Tests for common models."""
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from common.models import RandomModel


class RandomModelTests(TestCase):
    """Tests für RandomModel."""

    def test_object_save_with_database_constraint_fails_with_validation_error_when_full_cleaned(self):
        """Test that saving an object with invalid dates raises a ValidationError."""
        start_date = timezone.now().date()
        end_date = start_date - timedelta(days=1)

        with self.assertRaises(ValidationError):
            obj = RandomModel(start_date=start_date, end_date=end_date)
            obj.full_clean()
            obj.save()

    def test_object_create_with_database_constraint_fails_with_integrity_error(self):
        """Test that creating an object with invalid dates raises an IntegrityError."""
        start_date = timezone.now().date()
        end_date = start_date - timedelta(days=1)

        with self.assertRaises(IntegrityError):
            RandomModel.objects.create(start_date=start_date, end_date=end_date)

    def test_object_can_be_created_when_constraint_is_not_hit(self):
        """Test that creating an object with valid dates works."""
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=1)

        self.assertEqual(0, RandomModel.objects.count())

        RandomModel.objects.create(start_date=start_date, end_date=end_date)

        self.assertEqual(1, RandomModel.objects.count())
