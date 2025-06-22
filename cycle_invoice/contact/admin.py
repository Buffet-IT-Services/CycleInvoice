"""Register the Contact models with the admin site."""

from django.contrib import admin

from cycle_invoice.common.models import BaseModelAdmin

from .models import Address, CompanyContact, Contact, Customer, Organisation

admin.site.register(Customer, BaseModelAdmin)
admin.site.register(Organisation, BaseModelAdmin)
admin.site.register(CompanyContact, BaseModelAdmin)
admin.site.register(Address, BaseModelAdmin)
admin.site.register(Contact, BaseModelAdmin)
