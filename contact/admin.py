"""Register the Contact model with the admin site."""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Address, CompanyContact, Contact, Organisation

admin.site.register(Contact, SimpleHistoryAdmin)
admin.site.register(Organisation, SimpleHistoryAdmin)
admin.site.register(CompanyContact, SimpleHistoryAdmin)
admin.site.register(Address, SimpleHistoryAdmin)
