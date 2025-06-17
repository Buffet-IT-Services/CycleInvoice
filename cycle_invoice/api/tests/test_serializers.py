"""Tests for the inline_serializer and create_serializer_class utilities."""
from django.test import TestCase
from rest_framework import serializers

from cycle_invoice.api.serializers import create_serializer_class, inline_serializer


class SerializersTest(TestCase):
    """Tests for the API serializers utilities."""

    def test_create_serializer_class(self) -> None:
        """Test creating a serializer class dynamically."""
        fields = {
            "name": serializers.CharField(),
            "age": serializers.IntegerField(),
        }
        test_serializer = create_serializer_class("test_serializer", fields)
        data = {"name": "Alice", "age": 30}
        serializer = test_serializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Alice")
        self.assertEqual(serializer.validated_data["age"], 30)

    def test_inline_serializer_with_data(self) -> None:
        """Test creating an inline serializer with data."""
        fields = {
            "title": serializers.CharField(),
            "amount": serializers.FloatField(),
        }
        data = {"title": "Invoice", "amount": 99.99}
        serializer = inline_serializer(fields=fields, data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["title"], "Invoice")
        self.assertEqual(serializer.validated_data["amount"], 99.99)

    def test_inline_serializer_without_data(self) -> None:
        """Test creating an inline serializer without data."""
        fields = {
            "active": serializers.BooleanField(),
        }
        serializer = inline_serializer(fields=fields)
        self.assertIsInstance(serializer, serializers.Serializer)
        self.assertIn("active", serializer.fields)

    def test_inline_serializer_unique_class(self) -> None:
        """Test that inline serializers create unique classes."""
        fields1 = {"a": serializers.IntegerField()}
        fields2 = {"b": serializers.CharField()}
        ser1 = inline_serializer(fields=fields1)
        ser2 = inline_serializer(fields=fields2)
        self.assertNotEqual(type(ser1), type(ser2))
        self.assertIn("a", ser1.fields)
        self.assertIn("b", ser2.fields)
