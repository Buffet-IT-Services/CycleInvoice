"""Factories for subscription app models."""

from factory import LazyAttribute, SubFactory

from cycle_invoice.common.tests.faker import faker
from cycle_invoice.common.tests.factories import BaseFactory
from cycle_invoice.party.tests.factories import OrganizationFactory
from cycle_invoice.product.tests.factories import ProductFactory
from cycle_invoice.subscription.models import SubscriptionPlan, Subscription


class SubscriptionPlanFactory(BaseFactory):
    """Factory for the SubscriptionPlan model."""

    class Meta:
        """Metaclass for SubscriptionPlanFactory."""

        model = SubscriptionPlan

    product = SubFactory(ProductFactory)
    price = LazyAttribute(lambda _self: _self.product.price)
    recurrence = "yearly"


class SubscriptionFactory(BaseFactory):
    """Factory for the Subscription model."""

    class Meta:
        """Metaclass for SubscriptionFactory."""

        model = Subscription

    plan = SubFactory(SubscriptionPlanFactory)
    party = SubFactory(OrganizationFactory)
    start_date = LazyAttribute(lambda _: faker.past_date())
