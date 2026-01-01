"""Constance settings for CycleInvoice."""

from django.utils.translation import gettext_lazy as _

# Set Constance backend to use the database
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_ADDITIONAL_FIELDS = {
    "image_field": ["django.forms.ImageField", {}],
}

# Directory within MEDIA_ROOT where Constance will store file-based settings
CONSTANCE_FILE_ROOT = "constance"

CONSTANCE_CONFIG = {
    "Company Logo": ("CycleInvoice.png", _("The logo of the company."), "image_field"),
    "Company Name": ("CycleInvoice", _("The name of the company."), str),
}

# Ordering the Fields to sets
CONSTANCE_CONFIG_FIELDSETS = (
    (
        _("Company Settings"),
        {
            "fields": ("Company Logo", "Company Name"),
        }
    ),
)
