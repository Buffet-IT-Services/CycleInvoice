"""Services for handling subscriptions."""
from django.db import transaction

from sale.models import Subscription, DocumentItemSubscription


class SubscriptionExtensionError(Exception):
    """Custom exception for subscription extension errors."""
    pass


@transaction.atomic
def subscription_extension(subscription_id: int) -> None:
    """Extends a subscription by one billing period.
    :param subscription_id:
    """
    subscription = Subscription.objects.get(id=subscription_id)
    if subscription.is_canceled is False:
        raise SubscriptionExtensionError(f"Subscription {subscription_id} is canceled and cannot be extended.")

    # calculate next start and end billed dates
    start = subscription.next_start_billed_date
    end = subscription.next_end_billed_date
    time_range = f"{start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}"

    # create DocumentItemSubscription
    DocumentItemSubscription.objects.create(
        product=subscription.product.product,
        subscription=subscription,
        time_range=time_range,
        customer=subscription.customer,
        price=subscription.product.price,
        quantity=1,
    )

    # update Subscription
    subscription.end_billed_date = end
    subscription.save()

