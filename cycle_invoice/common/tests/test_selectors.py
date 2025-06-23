"""Tests for common selectors."""
from django.test import TestCase

from cycle_invoice.common.models import TestBaseModel
from cycle_invoice.common.selectors import get_object
from cycle_invoice.common.tests.base import get_default_test_user


class GetObjectTest(TestCase):
    """Tests for the get_object selector."""

    def setUp(self) -> None:
        """Set up the test case with a default user and an instance of TestBaseModel."""
        self.default_user = get_default_test_user()
        self.instance = TestBaseModel()
        self.instance.save(user=self.default_user)

    def test_get_object_returns_instance_by_pk(self) -> None:
        """Test that get_object returns the instance by primary key."""
        obj = get_object(TestBaseModel, search_id=self.instance.pk)
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_instance_by_uuid(self) -> None:
        """Test that get_object returns the instance by primary key."""
        obj = get_object(TestBaseModel, search_id=self.instance.uuid)
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_instance_by_queryset_pk(self) -> None:
        """Test that get_object returns the instance from a queryset."""
        qs = TestBaseModel.objects.all()
        obj = get_object(qs, search_id=self.instance.pk)
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_instance_by_queryset_uuid(self) -> None:
        """Test that get_object returns the instance from a queryset."""
        qs = TestBaseModel.objects.all()
        obj = get_object(qs, search_id=self.instance.uuid)
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_none_if_not_found_int(self) -> None:
        """Test that get_object returns None if the instance is not found."""
        obj = get_object(TestBaseModel, search_id=99999)
        self.assertIsNone(obj)

    def test_get_object_returns_none_if_not_found_str(self) -> None:
        """Test that get_object returns None if the instance is not found."""
        obj = get_object(TestBaseModel, search_id="4398f182-3c41-480a-afc7-15387ce5511c")
        self.assertIsNone(obj)

    def test_get_object_with_queryset_returns_none_if_not_found_pk(self) -> None:
        """Test that get_object returns None if the instance is not found in a queryset."""
        qs = TestBaseModel.objects.all()
        obj = get_object(qs, search_id=99999)
        self.assertIsNone(obj)

    def test_get_object_with_queryset_returns_none_if_not_found_uuid(self) -> None:
        """Test that get_object returns None if the instance is not found in a queryset."""
        qs = TestBaseModel.objects.all()
        obj = get_object(qs, search_id="4398f182-3c41-480a-afc7-15387ce5511c")
        self.assertIsNone(obj)
