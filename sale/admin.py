"""A module for sale admin."""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from sale.models import DocumentItemSubscription, Product, Subscription, SubscriptionProduct, DocumentInvoice, \
    DocumentItemWork, WorkType

# Register your models here.
admin.site.register(Product, SimpleHistoryAdmin)
admin.site.register(SubscriptionProduct, SimpleHistoryAdmin)
admin.site.register(Subscription, SimpleHistoryAdmin)
admin.site.register(DocumentItemSubscription, SimpleHistoryAdmin)
admin.site.register(DocumentInvoice, SimpleHistoryAdmin)
admin.site.register(DocumentItemWork, SimpleHistoryAdmin)
admin.site.register(WorkType, SimpleHistoryAdmin)