"""Common selectors for Django models."""

from typing import TypeVar
from uuid import UUID

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models import Model, QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404

T = TypeVar("T", bound=Model)


def get_object[T](model_or_queryset: type[T] | QuerySet, *, include_deleted: bool = False, **kwargs) -> T | None:
    """
    Getter for Django models.

    :param model_or_queryset: A Django model class or a QuerySet.
    :param include_deleted: When False (default), excludes soft-deleted rows.

    :return: The model instance if found, else None.

    Some important notes:
        - `search_id`: accepts int, numeric string, or UUID string.
    """

    # Parse search_id into pk or uuid
    if "search_id" in kwargs:
        search_id = kwargs.pop("search_id")
        try:
            kwargs["pk"] = int(search_id)  # Attempt to parse as integer primary key
        except (TypeError, ValueError):
            try:
                kwargs["uuid"] = UUID(str(search_id))  # Attempt to parse as UUID
            except (ValueError, TypeError):
                error_message = f"search_id '{search_id}' is not a valid pk or UUID."
                raise ValueError(error_message)

    # Respect soft-delete by default
    if isinstance(model_or_queryset, QuerySet):
        queryset = model_or_queryset.filter(soft_deleted=False) if not include_deleted else model_or_queryset
    else:
        manager = (
            model_or_queryset.objects_with_deleted
            if include_deleted and hasattr(model_or_queryset, "objects_with_deleted")
            else model_or_queryset.objects
        )
        queryset = manager.all()

    try:
        return get_object_or_404(queryset, **kwargs)
    except Http404:
        return None


def get_model_fields(instance: models.Model) -> dict[str, models.Field]:
    """
    Returns a dict of model fields for a Django model instance.

    :param instance: A Django model instance.

    :return: A dictionary mapping field names to their corresponding Field objects.
    """
    return {field.name: field for field in instance._meta.get_fields()}  # noqa: SLF001


def get_system_user() -> AbstractBaseUser:
    """
    Return the system user that is used for automated/system tasks.

    :return: An AbstractBaseUser instance representing the system user.
    """
    user_model = get_user_model()
    return user_model.objects.get(email="system@cycleinvoice.local")
