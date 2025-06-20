"""Admin configuration for the subscription app."""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from cycle_invoice.subscription.models import SubscriptionProduct, Subscription

# Register your models here.
admin.site.register(SubscriptionProduct, SimpleHistoryAdmin)
admin.site.register(Subscription, SimpleHistoryAdmin)
