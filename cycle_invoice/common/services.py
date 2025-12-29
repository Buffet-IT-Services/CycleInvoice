"""Common services for Django models."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cycle_invoice.common.selectors import get_model_fields

if TYPE_CHECKING:
    from cycle_invoice.common.models import BaseModel, User
    from cycle_invoice.common.types import DjangoModelType


def model_update(instance: BaseModel, fields: list[str], data: dict[str, Any], user: User) \
        -> tuple[DjangoModelType, bool]:
    """
    Update service for Django models.

    :param instance: The model instance that should be updated.
    :param fields: A list of field names that should be updated.
    :param data: A dictionary containing the new values for the fields.
    :param user: Pass the user performing the update, used for setting `updated_by`.

    :return: A tuple containing the updated instance and a boolean indicating whether any fields were updated.

    Some important notes:
        - Only keys present in `fields` will be taken from `data`.
        - If something is present in `fields` but not present in `data`, we simply skip.
        - There's a strict assertion that all values in `fields` are actual fields in `instance`.
        - `fields` can support m2m fields, which are handled after the update on `instance
        - `soft_deleted` objects cannot be updated.
    """
    # Reject updates on soft-deleted objects
    if getattr(instance, "soft_deleted", False):
        error_message = f"Cannot update a soft-deleted {instance.__class__.__name__}."
        raise ValueError(error_message)

    # Reject updates if the user is not of the expected type
    from cycle_invoice.common.models import User as UserModel  # noqa: PLC0415 (to avoid circular import)
    if user is None or not isinstance(user, UserModel):
        error_message = "User of type 'User' must be provided."
        raise ValueError(error_message)

    has_updated = False
    update_fields: list[str] = []

    model_fields = get_model_fields(instance)

    for field in fields:

        # Skip if a field is not present in the actual data
        if field not in data:
            continue

        # If a field is not an actual model field, raise an error
        model_field = model_fields.get(field)
        if model_field is None:
            error_message = f"Field '{field}' is not part of {instance.__class__.__name__}."
            raise ValueError(error_message)

        # Update only if the value has changed
        if getattr(instance, field) != data[field]:
            has_updated = True
            update_fields.append(field)
            setattr(instance, field, data[field])

    # Perform an update only if any of the fields were actually changed
    if has_updated:
        instance.full_clean()
        instance.save(user=user)

    return instance, has_updated
