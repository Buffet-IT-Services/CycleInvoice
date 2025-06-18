"""Common selectors for Django models."""
from typing import TypeVar

from django.db.models import Model, QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404

T = TypeVar("T", bound=Model)


def get_object[T](model_or_queryset: type[T] | QuerySet, **kwargs) -> T | None:
    """Reuses get_object_or_404, catches Http404 and returns None."""
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None
