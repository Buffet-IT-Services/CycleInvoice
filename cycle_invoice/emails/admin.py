"""Admin configuration for emails app."""

from django.contrib import admin

from cycle_invoice.common.models import BaseModelAdmin
from cycle_invoice.emails.models import Email

admin.site.register(Email, BaseModelAdmin)
