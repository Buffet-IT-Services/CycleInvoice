"""Common services for Django models."""
from typing import Any

from django.db import models
from django.utils import timezone

from cycle_invoice.common.types import DjangoModelType


def model_update(*, instance: DjangoModelType, fields: list[str], data: dict[str, Any],
                 auto_updated_at: bool = True) -> tuple[DjangoModelType, bool]:
    """
    Update service for Django models.

    :param instance: The model instance to be updated.
    :param fields: A list of field names that should be updated.
    :param data: A dictionary containing the new values for the fields.
    :param auto_updated_at: If True, will automatically update the `updated_at` field if it exists.

    :return: A tuple containing the updated instance and a boolean indicating whether any fields were updated.

    Some important notes:
        - Only keys present in `fields` will be taken from `data`.
        - If something is present in `fields` but not present in `data`, we simply skip.
        - There's a strict assertion that all values in `fields` are actual fields in `instance`.
        - `fields` can support m2m fields, which are handled after the update on `instance`.
        - If `auto_updated_at` is True, we'll try bumping `updated_at` with the current timestmap.
    """
    has_updated = False
    m2m_data = {}
    update_fields = []

    model_fields = get_model_fields(instance)

    for field in fields:
        # Skip if a field is not present in the actual data
        if field not in data:
            continue

        # If field is not an actual model field, raise an error
        model_field = model_fields.get(field)

        if model_field is None:
            error_message = f"Field '{field}' is not part of {instance.__class__.__name__}"
            raise AssertionError(error_message)

        # If we have m2m field, handle differently
        if isinstance(model_field, models.ManyToManyField):
            m2m_data[field] = data[field]
            continue

        if getattr(instance, field) != data[field]:
            has_updated = True
            update_fields.append(field)
            setattr(instance, field, data[field])

    # Perform an update only if any of the fields were actually changed
    if has_updated:
        if auto_updated_at and "updated_at" in model_fields:
            update_fields.append("updated_at")
            instance.updated_at = timezone.now()

        instance.full_clean()

        # Update only the fields that are meant to be updated.
        instance.save(update_fields=update_fields)

    for field_name, value in m2m_data.items():
        related_manager = getattr(instance, field_name)
        related_manager.set(value)

    return instance, has_updated


def get_model_fields(instance: models.Model) -> dict[str, models.Field]:
    """Return a dict of model fields for a Django model instance."""
    return {field.name: field for field in instance._meta.get_fields()} # noqa: SLF001
