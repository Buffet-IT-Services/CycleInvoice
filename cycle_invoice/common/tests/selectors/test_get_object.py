"""Tests for the common selector method get_object[T]() -> T | None."""
from uuid import UUID

from django.test import TestCase

from cycle_invoice.common.models import User
from cycle_invoice.common.selectors import get_object
from cycle_invoice.common.tests.factories import UserFactory


class TestGetObject(TestCase):
    """Tests for the common selector method get_object[T]() -> T | None."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.instance = UserFactory.create()

    def test_get_object_returns_instance_by_pk(self) -> None:
        """Test get_object() with a valid primary key."""
        obj = get_object(User, pk=self.instance.pk)
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_instance_by_pk_string(self) -> None:
        """Test get_object() with a valid primary key."""
        obj = get_object(User, pk=str(self.instance.pk))
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_instance_by_uuid(self) -> None:
        """Test get_object() with a valid UUID."""
        obj = get_object(User, uuid=self.instance.uuid)
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_instance_by_uuid_string(self) -> None:
        """Test get_object() with a valid UUID."""
        obj = get_object(User, uuid=str(self.instance.uuid))
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_none_for_invalid_uuid(self) -> None:
        """Test get_object() with an invalid UUID."""
        obj = get_object(User, uuid=UUID("4398f182-3c41-480a-afc7-15387ce5511c"))
        self.assertIsNone(obj)

    def test_get_object_returns_none_for_invalid_uuid_string(self) -> None:
        """Test get_object() with an invalid UUID."""
        obj = get_object(User, uuid="4398f182-3c41-480a-afc7-15387ce5511c")
        self.assertIsNone(obj)

    def test_get_object_returns_instance_by_pk_with_queryset(self) -> None:
        """Test get_object() with a valid primary key and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, pk=self.instance.pk)
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_instance_by_pk_string_with_queryset(self) -> None:
        """Test get_object() with a valid primary key and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, pk=str(self.instance.pk))
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_none_for_invalid_pk_with_queryset(self) -> None:
        """Test get_object() with an invalid primary key and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, pk=999999)
        self.assertIsNone(obj)

    def test_get_object_returns_instance_by_uuid_with_queryset(self) -> None:
        """Test get_object() with a valid UUID and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, uuid=self.instance.uuid)
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_instance_by_uuid_string_with_queryset(self) -> None:
        """Test get_object() with a valid UUID and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, uuid=str(self.instance.uuid))
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_none_for_invalid_uuid_with_queryset(self) -> None:
        """Test get_object() with an invalid UUID and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, uuid=UUID("4398f182-3c41-480a-afc7-15387ce5511c"))
        self.assertIsNone(obj)

    def test_get_object_returns_none_for_invalid_uuid_string_with_queryset(self) -> None:
        """Test get_object() with an invalid UUID and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, uuid="4398f182-3c41-480a-afc7-15387ce5511c")
        self.assertIsNone(obj)

    def test_get_object_returns_instance_by_pk_as_search_id(self) -> None:
        """Test get_object() with a valid primary key."""
        obj = get_object(User, search_id=self.instance.pk)
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_instance_by_pk_string_as_search_id(self) -> None:
        """Test get_object() with a valid primary key."""
        obj = get_object(User, search_id=str(self.instance.pk))
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_none_for_invalid_pk_as_search_id(self) -> None:
        """Test get_object() with an invalid primary key."""
        obj = get_object(User, search_id=999999)
        self.assertIsNone(obj)

    def test_get_object_returns_none_for_invalid_pk_string_as_search_id(self) -> None:
        """Test get_object() with an invalid primary key."""
        obj = get_object(User, search_id=str(999999))
        self.assertIsNone(obj)

    def test_get_object_returns_instance_by_uuid_as_search_id(self) -> None:
        """Test get_object() with a valid UUID."""
        obj = get_object(User, search_id=self.instance.uuid)
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_instance_by_uuid_string_as_search_id(self) -> None:
        """Test get_object() with a valid UUID."""
        obj = get_object(User, search_id=str(self.instance.uuid))
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_none_for_invalid_uuid_as_search_id(self) -> None:
        """Test get_object() with an invalid UUID."""
        obj = get_object(User, search_id=UUID("4398f182-3c41-480a-afc7-15387ce5511c"))
        self.assertIsNone(obj)

    def test_get_object_returns_none_for_invalid_uuid_string_as_search_id(self) -> None:
        """Test get_object() with an invalid UUID."""
        obj = get_object(User, search_id="4398f182-3c41-480a-afc7-15387ce5511c")
        self.assertIsNone(obj)

    def test_get_object_returns_instance_by_pk_with_queryset_as_search_id(self) -> None:
        """Test get_object() with a valid primary key and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, search_id=self.instance.pk)
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_instance_by_pk_string_with_queryset_as_search_id(self) -> None:
        """Test get_object() with a valid primary key and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, search_id=str(self.instance.pk))
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_none_for_invalid_pk_with_queryset_as_search_id(self) -> None:
        """Test get_object() with an invalid primary key and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, search_id=999999)
        self.assertIsNone(obj)

    def test_get_object_returns_none_for_invalid_pk_string_with_queryset_as_search_id(self) -> None:
        """Test get_object() with an invalid primary key and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, search_id=str(999999))
        self.assertIsNone(obj)

    def test_get_object_returns_instance_by_uuid_with_queryset_as_search_id(self) -> None:
        """Test get_object() with a valid UUID and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, search_id=self.instance.uuid)
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_instance_by_uuid_string_with_queryset_as_search_id(self) -> None:
        """Test get_object() with a valid UUID and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, search_id=str(self.instance.uuid))
        self.assertEqual(obj, self.instance)

    def test_get_object_returns_none_for_invalid_uuid_with_queryset_as_search_id(self) -> None:
        """Test get_object() with an invalid UUID and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, search_id=UUID("4398f182-3c41-480a-afc7-15387ce5511c"))
        self.assertIsNone(obj)

    def test_get_object_returns_none_for_invalid_uuid_string_with_queryset_as_search_id(self) -> None:
        """Test get_object() with an invalid UUID and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, search_id="4398f182-3c41-480a-afc7-15387ce5511c")
        self.assertIsNone(obj)

    def test_get_object_returns_none_for_random_string(self) -> None:
        """Test get_object() with a random string."""
        obj = get_object(User, search_id="random")
        self.assertIsNone(obj)

    def test_get_object_returns_none_for_empty_string(self) -> None:
        """Test get_object() with an empty string."""
        obj = get_object(User, search_id="")
        self.assertIsNone(obj)

    def test_get_object_returns_none_for_random_string_with_queryset(self) -> None:
        """Test get_object() with a random string and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, search_id="random")
        self.assertIsNone(obj)

    def test_get_object_returns_none_for_empty_string_with_queryset(self) -> None:
        """Test get_object() with an empty string and a queryset."""
        queryset = User.objects.all()
        obj = get_object(queryset, search_id="")
        self.assertIsNone(obj)
