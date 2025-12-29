"""A module for sale admin."""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from cycle_invoice.sale.models import (
    DocumentItem,
    Invoice,
)

admin.site.register(Invoice, SimpleHistoryAdmin)
admin.site.register(DocumentItem, SimpleHistoryAdmin)
