"""Test cases for the DocumentItemSubscription model."""

from django.test import TestCase

from contact.tests.models.test_contact import fake_contact
from sale.models import DocumentItemSubscription
from sale.tests.models.test_subscription import fake_subscription


def fake_document_item_subscription() -> DocumentItemSubscription:
    """Create a fake document item subscription."""
    subscription = fake_subscription()
    product = subscription.product.product
    return DocumentItemSubscription.objects.create(subscription=subscription, time_range="Monthly", product=product,
                                                   price=10.00, quantity=1, customer=fake_contact())


class DocumentItemSubscriptionTest(TestCase):
    """Test cases for the DocumentItemSubscription model."""

    def test_title_str(self) -> None:
        """Test the title_str property."""
        item = fake_document_item_subscription()
        self.assertEqual("Test Product (Monthly)", item.title_str)

    def test_comment_str(self) -> None:
        """Test the comment_str property."""
        item = fake_document_item_subscription()
        self.assertEqual(item.product.description, item.comment_str)
