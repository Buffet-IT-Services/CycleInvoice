"""Product module admin config."""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from cycle_invoice.product.models import Product

# Register your models here.
admin.site.register(Product, SimpleHistoryAdmin)
