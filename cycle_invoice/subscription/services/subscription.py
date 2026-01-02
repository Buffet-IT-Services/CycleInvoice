"""Services for handling subscriptions."""

from django.contrib.auth import get_user_model
from django.db import transaction

from cycle_invoice.common.selectors import get_object
from cycle_invoice.subscription.models import Subscription, SubscriptionDocumentItem


class SubscriptionExtensionError(Exception):
    """Custom exception for subscription extension errors."""


@transaction.atomic
def subscription_extension(subscription: Subscription | int, user: get_user_model) -> None:
    """
    Extend a subscription by one billing period.

    :param subscription: Subscription instance or identifier.
    :param user: User who is extending the subscription.
    """
    if subscription is None:
        error_message = "Subscription must be provided."
        raise ValueError(error_message)

    if isinstance(subscription, Subscription):
        subscription_obj = subscription
        subscription_id = subscription_obj.id
    else:
        subscription_obj = get_object(model_or_queryset=Subscription, search_id=subscription)
        subscription_id = subscription

    if subscription_obj is None:
        error_message = f"Subscription {subscription_id} does not exist."
        raise ValueError(error_message)

    if subscription_obj.is_cancelled:
        error_message = f"Subscription {subscription_id} is canceled and cannot be extended."
        raise SubscriptionExtensionError(error_message)

    if user is None or not isinstance(user, get_user_model()):
        error_message = "User of type 'User' must be provided."
        raise ValueError(error_message)

    # calculate next start and end billed dates
    start = subscription_obj.next_start_billed_date
    end = subscription_obj.next_end_billed_date
    time_range = f"{start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}"

    # create SubscriptionDocumentItem
    subscription_document_item = SubscriptionDocumentItem(
        price=subscription_obj.plan.price,
        quantity=1,
        document=None,
        title=f"{subscription_obj.plan.product.name} - {time_range}",
        description=subscription_obj.plan.product.description,
        party=subscription_obj.party,
        account=subscription_obj.plan.product.account_sell,
        discount_value=subscription_obj.discount_value,
        discount_type=subscription_obj.discount_type,
        subscription=subscription_obj
    )
    subscription_document_item.save(user=user)

    # update Subscription
    subscription_obj.end_billed_date = end
    subscription_obj.save(user=user)
