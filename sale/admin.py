"""A module for sale admin."""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from sale.models import (
    DocumentInvoice,
    Product,
    Subscription,
    SubscriptionProduct,
    WorkType, DocumentItem,
)

# Register your models here.
admin.site.register(Product, SimpleHistoryAdmin)
admin.site.register(SubscriptionProduct, SimpleHistoryAdmin)
admin.site.register(Subscription, SimpleHistoryAdmin)
admin.site.register(DocumentInvoice, SimpleHistoryAdmin)
admin.site.register(WorkType, SimpleHistoryAdmin)
admin.site.register(DocumentItem, SimpleHistoryAdmin)
