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
    "COMPANY_LOGO": ("CycleInvoice.png", _("The logo of the company."), "image_field"),
    "COMPANY_NAME": ("CycleInvoice", _("The name of the company."), str),

    "COMPANY_EMAIL_SEND": ("'CycleInvoice NoReply' <noreply@cycleinvoice.local>",
                           _("The email address to send emails from."), str),
    "COMPANY_EMAIL_REPLY_TO": ("'CycleInvoice Support' <support@cycleinvoice.local>",
                               _("The email address to reply to emails from."), str),
}

# Ordering the Fields to sets
CONSTANCE_CONFIG_FIELDSETS = (
    (
        _("Company Settings"),
        {
            "fields": ("COMPANY_LOGO", "COMPANY_NAME"),
        },
    ),
    (
        _("Email Settings"),
        {
            "fields": ("COMPANY_EMAIL_SEND", "COMPANY_EMAIL_REPLY_TO"),
        }
    ),
)
