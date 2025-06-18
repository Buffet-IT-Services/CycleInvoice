"""Services for handling subscriptions."""
from django.contrib.auth import get_user_model
from django.db import transaction

from cycle_invoice.sale.models import DocumentItem, Subscription


class SubscriptionExtensionError(Exception):
    """Custom exception for subscription extension errors."""


@transaction.atomic
def subscription_extension(subscription_id: int, user: get_user_model) -> None:
    """
    Extend a subscription by one billing period.

    :param subscription_id:
    :param user: User who is extending the subscription
    """
    subscription = Subscription.objects.get(id=subscription_id)
    if subscription.is_cancelled is True:
        error_message = f"Subscription {subscription_id} is canceled and cannot be extended."
        raise SubscriptionExtensionError(error_message)

    # calculate next start and end billed dates
    start = subscription.next_start_billed_date
    end = subscription.next_end_billed_date
    time_range = f"{start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}"

    # create DocumentItemSubscription
    document_item = DocumentItem(
        product=subscription.product.product,
        subscription=subscription,
        comment_title=time_range,
        customer=subscription.customer,
        price=subscription.product.price,
        quantity=1,
        item_type="subscription",
    )
    document_item.save(user=user)

    # update Subscription
    subscription.end_billed_date = end
    subscription.save(user=user)
