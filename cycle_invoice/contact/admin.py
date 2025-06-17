"""Register the Contact models with the admin site."""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Address, CompanyContact, Contact, Customer, Organisation

admin.site.register(Customer, SimpleHistoryAdmin)
admin.site.register(Contact, SimpleHistoryAdmin)
admin.site.register(Organisation, SimpleHistoryAdmin)
admin.site.register(CompanyContact, SimpleHistoryAdmin)
admin.site.register(Address, SimpleHistoryAdmin)
