"""Models for the contact app."""
import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import ChangeLoggerAll

logger = logging.getLogger(__name__)


class Customer(ChangeLoggerAll):
    """Model representing a customer."""

    address = models.ForeignKey(
        "Address",
        on_delete=models.PROTECT,
        related_name="organisations",
        verbose_name=_("address"),
        null=True,
        blank=True,
    )

    class Meta:
        """Meta options for the Customer model."""

        verbose_name = _("customer")
        verbose_name_plural = _("customers")

    def __str__(self) -> str:
        """Return a string representation of the customer."""
        if hasattr(self, 'contact'):
            return str(self.contact)
        elif hasattr(self, 'organisation'):
            return str(self.organisation)
        return "Customer (unknown type)"

    @property
    def address_block(self) -> str:
        """Return the address block for the customer."""
        if self.address is not None:
            return str(self) + "\n" + address_block(self.address)
        return str(self)


class Organisation(Customer):
    """Model representing an organisation."""

    name = models.CharField(_("name"), max_length=255, unique=True)
    email = models.EmailField(_("email"), max_length=255, blank=True)
    phone = models.CharField(_("phone"), max_length=20, blank=True)
    uid = models.CharField(_("uid"), max_length=20, unique=True, blank=True, null=True)

    class Meta:
        """Meta options for the Organisation model."""

        verbose_name = _("company")
        verbose_name_plural = _("companies")

    def __str__(self) -> str:
        """Return a string representation of the organisation."""
        return self.name


class Contact(Customer):
    """Model representing a contact."""

    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)
    email = models.EmailField(_("email"), max_length=255, blank=True)
    phone = models.CharField(_("phone"), max_length=20, blank=True)
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


class Address(ChangeLoggerAll):
    """Model representing an address."""

    additional = models.CharField(_("additional"), max_length=255, blank=True)
    street = models.CharField(_("street"), max_length=255)
    number = models.CharField(_("number"), max_length=10)
    city = models.CharField(_("city"), max_length=255)
    zip_code = models.CharField(_("zip code"), max_length=12)
    country = models.CharField(_("country"), max_length=255)
    disabled = models.BooleanField(default=False)

    class Meta:
        """Meta options for the Address model."""

        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self) -> str:
        """Return a string representation of the address."""
        additional = f"{self.additional}, " if self.additional else ""
        return f"{additional}{self.street} {self.number}, {self.zip_code} {self.city}, {self.country}"

    def save(self, *args, **kwargs) -> None:
        """Override save method to handle address changes and references."""
        logger.debug("Saving address: %s", self)
        from vehicle.models import DocumentItemKilometers
        if self.pk:
            # Check if this address is referenced by a DocumentItemKilometers object
            from django.db.models import Q
            is_referenced = DocumentItemKilometers.objects.filter(
                Q(start_address=self) | Q(end_address=self)
            ).exists()
            if is_referenced:
                # Check if any fields except 'additional' have changed
                old = type(self).objects.get(pk=self.pk)
                main_fields = ["street", "number", "city", "zip_code", "country"]
                changed_main = any(getattr(self, f) != getattr(old, f) for f in main_fields)
                if changed_main:
                    logger.info("Address '%s' is referenced by DocumentItemKilometers, creating new.", self)
                    # Set old object to disabled = True and create a new object
                    old_pk = self.pk
                    type(self).objects.filter(pk=old_pk).update(disabled=True)
                    self.pk = None
                    super().save(*args, **kwargs)
                    # Update all customers referencing the old address to the new address
                    customers = self._meta.apps.get_model("contact", "Customer")
                    customers.objects.filter(address_id=old_pk).update(address=self)
                    return
        super().save(*args, **kwargs)


def address_block(address: Address) -> str:
    """Return the address block for the given address."""
    additional = f"{address.additional}\n" if address.additional else ""
    return f"{additional}{address.street} {address.number}\n{address.zip_code} {address.city}\n{address.country}"
