"""A module for sale admin."""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from sale.models import Product, Subscription, SubscriptionProduct

# Register your models here.
admin.site.register(Product, SimpleHistoryAdmin)
admin.site.register(SubscriptionProduct, SimpleHistoryAdmin)
admin.site.register(Subscription, SimpleHistoryAdmin)
