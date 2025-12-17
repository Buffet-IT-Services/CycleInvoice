"""Common selectors for Django models."""
from typing import TypeVar
from uuid import UUID

from django.db.models import Model, QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404

T = TypeVar("T", bound=Model)


def get_object[T](model_or_queryset: type[T] | QuerySet, *, include_deleted: bool = False, **kwargs) -> T | None:
    """
    Reuses get_object_or_404, catches Http404 and returns None.

    Enhancements:
    - `search_id`: accepts int, numeric string, or UUID string.
    - `include_deleted`: when False (default), excludes soft-deleted rows if possible.
    """
    # Parse search_id into pk or uuid
    if "search_id" in kwargs:
        search_id = kwargs.pop("search_id")
        parsed = False
        # Try integer primary key (also handles numeric strings)
        try:
            kwargs["pk"] = int(search_id)  # type: ignore[arg-type]
            parsed = True
        except (TypeError, ValueError):
            pass
        if not parsed:
            # Try UUID
            try:
                kwargs["uuid"] = UUID(str(search_id))
                parsed = True
            except (ValueError, TypeError):
                pass
        if not parsed:
            # Fallback: pass as pk
            kwargs["pk"] = search_id

    # Respect soft-delete by default
    queryset: QuerySet | None = None
    if isinstance(model_or_queryset, QuerySet):
        queryset = model_or_queryset
        if not include_deleted:
            queryset = queryset.filter(soft_deleted=False)
    else:
        # A model class was provided; prefer appropriate manager
        model_cls = model_or_queryset
        if include_deleted and hasattr(model_cls, "objects_with_deleted"):
            queryset = model_cls.objects_with_deleted.all()
        else:
            queryset = model_cls.objects.all()

    try:
        return get_object_or_404(queryset, **kwargs)
    except Http404:
        return None
