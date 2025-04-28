"""Register the Account models with the admin site."""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Account

admin.site.register(Account, SimpleHistoryAdmin)

from extra_settings.admin import register_extra_settings_admin

register_extra_settings_admin(
    app=__name__,
    queryset_processor=lambda qs: qs.filter(name__istartswith="VIDEOS_"),
    unregister_default=True,
)