from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import ChangeLoggerAll
from contact.models import Organisation
from sale.models import SaleProduct, SubscriptionItem


# Create your models here.
class Domain(ChangeLoggerAll):
    """Model representing a sale work item."""

    customer = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="domain_customer",
        verbose_name=_("customer"),
    )
    domain_name = models.CharField(
        max_length=255,
        verbose_name=_("domain name"),
        unique=True,
    )

    class Meta:
        """Meta options for the Domain model."""

        verbose_name = _("domain")
        verbose_name_plural = _("domains")

    def __str__(self) -> str:
        """Return a string representation of the domain."""
        return self.domain_name


class HostingSubscription(SubscriptionItem):
    """Model representing a hosting."""

    customer = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="hosting_customer",
        verbose_name=_("customer"),
    )
    hosting_product = models.ForeignKey(
        SaleProduct,
        on_delete=models.CASCADE,
        related_name="hosting_product",
        verbose_name=_("hosting product"),
    )
    custom_price = models.DecimalField(_("price"), null=True, max_digits=10, decimal_places=2)

    class Meta:
        """Meta options for the Hosting model."""

        verbose_name = _("hosting")
        verbose_name_plural = _("hostings")

    def __str__(self) -> str:
        """Return a string representation of the hosting."""
        return f"{self.customer} - {self.hosting_product}"


class HostingProduct(SaleProduct):
    """Model representing a hosting product."""

    storage_capacity = models.PositiveIntegerField(
        _("storage capacity (GB)"),
        default=0,
    )
    price_yearly = models.DecimalField(_("price per year"), max_digits=10, decimal_places=2)
    price_monthly = models.DecimalField(_("price per month"), max_digits=10, decimal_places=2)

    class Meta:
        """Meta options for the HostingProduct model."""

        verbose_name = _("hosting product")
        verbose_name_plural = _("hosting products")

    def __str__(self) -> str:
        """Return a string representation of the HostingProduct."""
        return f"{self.name} - {self.storage_capacity} GB"
