"""Register the Contact models with the admin site."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import BaseModelAdmin, User


@admin.register(User)
class CustomUserAdmin(BaseModelAdmin, DjangoUserAdmin):
    """Admin interface for the custom User model."""

    model = User

    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active", "last_login")
    list_filter = ("is_staff", "is_active", "is_superuser", "soft_deleted")
    search_fields = ("email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
        ("Audit", {"fields": ("uuid", "created_at", "updated_at", "created_by", "updated_by", "soft_deleted")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_superuser", "is_active", "groups",
                       "user_permissions"),
        }),
    )

    # Keep BaseModelAdmin protections and history-related read-only fields
    readonly_fields = BaseModelAdmin.readonly_fields
    filter_horizontal = ("groups", "user_permissions")
