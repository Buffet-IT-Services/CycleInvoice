"""Models for the contact app."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import ChangeLoggerAll


class Organisation(ChangeLoggerAll):
    """Model representing an organisation."""

    name = models.CharField(_("name"), max_length=255, unique=True)
    email = models.EmailField(_("email"), max_length=255)
    phone = models.CharField(_("phone"), max_length=20)
    address = models.ForeignKey(
        "Address",
        on_delete=models.PROTECT,
        related_name="organisations",
        verbose_name=_("address"),
        null=True,
        blank=True,
    )
    uid = models.CharField(_("uid"), max_length=20, unique=True)

    class Meta:
        """Meta options for the Organisation model."""

        verbose_name = _("company")
        verbose_name_plural = _("companies")

    def __str__(self) -> str:
        """Return a string representation of the organisation."""
        return self.name


class Contact(ChangeLoggerAll):
    """Model representing a contact."""

    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)
    email = models.EmailField(_("email"), max_length=255)
    phone = models.CharField(_("phone"), max_length=20)
    address = models.ForeignKey(
        "Address", on_delete=models.PROTECT, related_name="contacts", verbose_name=_("address"), null=True, blank=True
    )
    company = models.ManyToManyField(Organisation, through="CompanyContact")

    class Meta:
        """Meta options for the Contact model."""

        verbose_name = _("contact")
        verbose_name_plural = _("contacts")

    def __str__(self) -> str:
        """Return a string representation of the contact."""
        return f"{self.first_name} {self.last_name}"


class CompanyContact(ChangeLoggerAll):
    """Model representing a company contact."""

    company = models.ForeignKey(Organisation, on_delete=models.CASCADE, verbose_name=_("company"))
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name=_("contact"))
    role = models.CharField(_("role"), max_length=255)

    class Meta:
        """Meta options for the CompanyContact model."""

        verbose_name = _("company contact")
        verbose_name_plural = _("company contacts")
        constraints = [models.UniqueConstraint(fields=["company", "contact"], name="unique_company_contact")]

    def __str__(self) -> str:
        """Return a string representation of the company contact."""
        return f"{self.company} - {self.contact} - {self.role}"


class Address(models.Model):
    """Model representing an address."""

    street = models.CharField(_("street"), max_length=255)
    number = models.CharField(_("number"), max_length=10)
    city = models.CharField(_("city"), max_length=255)
    zip_code = models.CharField(_("zip code"), max_length=12)
    country = models.CharField(_("country"), max_length=255)

    class Meta:
        """Meta options for the Address model."""

        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self) -> str:
        """Return a string representation of the address."""
        return f"{self.street} {self.number}, {self.zip_code} {self.city}, {self.country}"
