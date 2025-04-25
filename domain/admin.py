"""Register the Domain models with the admin site."""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Domain, HostingProduct, HostingSubscription

admin.site.register(Domain, SimpleHistoryAdmin)
admin.site.register(HostingProduct, SimpleHistoryAdmin)
admin.site.register(HostingSubscription, SimpleHistoryAdmin)