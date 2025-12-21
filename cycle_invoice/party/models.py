"""Models for the party app."""
import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from cycle_invoice.common.models import BaseModel

logger = logging.getLogger(__name__)


class Party(BaseModel):
    """Model representing a party."""

    address = models.OneToOneField(
        "Address",
        on_delete=models.PROTECT,
        related_name="address",
        verbose_name=_("address"),
        null=True,
        blank=True,
    )
    email = models.EmailField(
        _("email"),
        max_length=255,
        blank=True
    )
    phone = models.CharField(
        _("phone"),
        max_length=20,
        blank=True
    )

    class Meta:
        """Meta-options for the Party model."""

        verbose_name = _("party")
        verbose_name_plural = _("parties")

    def __str__(self) -> str:
        """Return a string representation of the party."""
        if hasattr(self, "contact"):
            return str(self.contact)
        if hasattr(self, "organisation"):
            return str(self.organisation)
        raise ValueError("Party is no contact or organisation.")

    @property
    def address_block(self) -> str:
        """Return the address block for the customer."""
        if self.address is not None:
            return str(self) + "\n" + address_block(self.address)
        return str(self)


class Organization(Party):
    """Model representing an organisation."""

    name = models.CharField(
        _("name"),
        max_length=255,
        unique=True
    )
    uid = models.CharField(
        _("uid"),
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    class Meta:
        """Meta-options for the Organization model."""

        verbose_name = _("company")
        verbose_name_plural = _("companies")

    def __str__(self) -> str:
        """Return a string representation of the organization."""

        return self.name


class Contact(Party):
    """Model representing a contact."""

    first_name = models.CharField(
        _("first name"),
        max_length=255
    )
    last_name = models.CharField(
        _("last name"),
        max_length=255
    )
    organization = models.ManyToManyField(
        Organization,
        through="OrganizationContact"
    )

    class Meta:
        """Meta-options for the Contact model."""

        verbose_name = _("contact")
        verbose_name_plural = _("contacts")

    def __str__(self) -> str:
        """Return a string representation of the contact."""
        return f"{self.first_name} {self.last_name}"


class OrganizationContact(BaseModel):
    """Model representing a organization contact."""

    company = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name=_("company")
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        verbose_name=_("contact")
    )
    role = models.CharField(
        _("role"),
        max_length=255
    )

    class Meta:
        """Meta-options for the CompanyContact model."""

        verbose_name = _("company contact")
        verbose_name_plural = _("company contacts")
        constraints = [models.UniqueConstraint(fields=["company", "contact"], name="unique_company_contact")]

    def __str__(self) -> str:
        """Return a string representation of the company contact."""
        return f"{self.company} - {self.contact} - {self.role}"


class Address(BaseModel):
    """Model representing an address."""

    additional = models.CharField(
        _("additional"),
        max_length=255,
        blank=True
    )
    street = models.CharField(
        _("street"),
        max_length=255
    )
    number = models.CharField(
        _("number"),
        max_length=10
    )
    city = models.CharField(
        _("city"),
        max_length=255
    )
    zip_code = models.CharField(
        _("zip code"),
        max_length=12
    )
    country = models.CharField(
        _("country"),
        max_length=255
    )

    class Meta:
        """Meta-options for the Address model."""

        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self) -> str:
        """Return a string representation of the address."""
        additional = f"{self.additional}, " if self.additional else ""
        return f"{additional}{self.street} {self.number}, {self.zip_code} {self.city}, {self.country}"


def address_block(address: Address) -> str:
    """Return the address block for the given address."""
    additional = f"{address.additional}\n" if address.additional else ""
    return f"{additional}{address.street} {address.number}\n{address.zip_code} {address.city}\n{address.country}"
