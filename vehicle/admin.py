"""Admin configuration for the vehicle app."""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from vehicle.models import Vehicle

admin.site.register(Vehicle, SimpleHistoryAdmin)
