"""Serializers for the api app."""

from rest_framework import serializers


def create_serializer_class(name: str, fields: dict) -> type:
    """Create a serializer class dynamically."""
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields: dict, data: dict | None = None, **kwargs) -> serializers.Serializer:
    """Create an inline serializer for use in DRF views."""
    # Important note if you are using `drf-spectacular`
    # Please refer to the following issue:
    # https://github.com/HackSoftware/Django-Styleguide/issues/105#issuecomment-1669468898
    # Since you might need to use unique names (uuids) for each inline serializer
    serializer_class = create_serializer_class(name="inline_serializer", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
