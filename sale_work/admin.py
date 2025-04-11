"""Admin configuration for the SaleWork model."""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from sale_work.models import SaleWork

# Register your models here.
admin.site.register(SaleWork, SimpleHistoryAdmin)
