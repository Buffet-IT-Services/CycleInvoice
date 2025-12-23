"""Admin configuration for the subscription app."""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from cycle_invoice.subscription.models import Subscription, SubscriptionPlan

# Register your models here.
admin.site.register(SubscriptionPlan, SimpleHistoryAdmin)
admin.site.register(Subscription, SimpleHistoryAdmin)
