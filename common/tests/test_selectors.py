"""Tests for common selectors."""
from datetime import date, timedelta

from django.test import TestCase

from common.models import SimpleModel, RandomModel
from common.selectors import get_object


class GetObjectSelectorTests(TestCase):
    """Tests for the get_object selector."""

    def setUp(self):
        """Set up test data."""
        self.simple = SimpleModel.objects.create(name="Test Simple")
        self.random = RandomModel.objects.create(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1)
        )
        self.random.simple_objects.add(self.simple)

    def test_get_object_existing(self):
        """Test retrieving an existing object."""
        obj = get_object(SimpleModel, id=self.simple.id)
        self.assertIsNotNone(obj)
        self.assertEqual(obj, self.simple)

    def test_get_object_non_existing(self):
        """Test retrieving a non-existing object."""
        obj = get_object(SimpleModel, id=99999)
        self.assertIsNone(obj)

    def test_get_object_with_queryset(self):
        """Test retrieving an object using a queryset."""
        qs = SimpleModel.objects.filter(name="Test Simple")
        obj = get_object(qs, id=self.simple.id)
        self.assertIsNotNone(obj)
        self.assertEqual(obj, self.simple)

    def test_get_object_with_queryset_not_found(self):
        """Test retrieving an object with a queryset that does not match."""
        qs = SimpleModel.objects.filter(name="DoesNotExist")
        obj = get_object(qs, id=self.simple.id)
        self.assertIsNone(obj)
