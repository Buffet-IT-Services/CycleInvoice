"""Register the Contact models with the admin site."""

from django.contrib import admin

from cycle_invoice.common.models import BaseModelAdmin

from .models import Address, Contact, Organization, OrganizationContact, Party

admin.site.register(Party, BaseModelAdmin)
admin.site.register(Organization, BaseModelAdmin)
admin.site.register(OrganizationContact, BaseModelAdmin)
admin.site.register(Address, BaseModelAdmin)
admin.site.register(Contact, BaseModelAdmin)
