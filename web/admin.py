"""Admin config for the web application."""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Domain

admin.site.register(Domain, SimpleHistoryAdmin)
