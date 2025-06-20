"""Admin config for accounting app."""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Account

admin.site.register(Account, SimpleHistoryAdmin)
