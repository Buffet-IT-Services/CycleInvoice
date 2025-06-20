"""Admin configuration for the work app."""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from cycle_invoice.work.models import WorkType

admin.site.register(WorkType, SimpleHistoryAdmin)