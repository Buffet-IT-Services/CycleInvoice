"""Services for handling subscriptions."""
import uuid

from django.contrib.auth import get_user_model
from django.db import transaction

from cycle_invoice.common.selectors import get_object
from cycle_invoice.subscription.models import Subscription, SubscriptionDocumentItem


class SubscriptionExtensionError(Exception):
    """Custom exception for subscription extension errors."""


@transaction.atomic
def subscription_extension(subscription_uuid: uuid.UUID, user: get_user_model) -> None:
    """
    Extend a subscription by one billing period.

    :param subscription_uuid: UUID of the subscription to be extended
    :param user: User extending the subscription
    """
    subscription = get_object(model_or_queryset=Subscription, search_id=subscription_uuid)

    if subscription is None:
        error_message = f"Subscription {subscription_uuid} does not exist."
        raise ValueError(error_message)

    if subscription.is_cancelled:
        error_message = f"Subscription {subscription_uuid} is canceled and cannot be extended."
        raise SubscriptionExtensionError(error_message)

    if user is None or not isinstance(user, get_user_model()):
        error_message = "User of type 'User' must be provided."
        raise ValueError(error_message)

    # calculate next start and end billed dates
    start = subscription.next_start_billed_date
    end = subscription.next_end_billed_date
    time_range = f"{start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}"

    # create SubscriptionDocumentItem
    subscription_document_item = SubscriptionDocumentItem(
        price=subscription.plan.price,
        quantity=1,
        document=None,
        title=f"{subscription.plan.product.name} - {time_range}",
        description=subscription.plan.product.description,
        party=subscription.party,
        account=subscription.plan.product.account_sell,
        discount_value=subscription.discount_value,
        discount_type=subscription.discount_type,
        subscription=subscription
    )
    subscription_document_item.save(user=user)

    # update Subscription
    subscription.end_billed_date = end
    subscription.save(user=user)
