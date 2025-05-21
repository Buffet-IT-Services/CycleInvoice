"""Test cases for the DocumentItemProduct model."""

from django.test import TestCase

from sale.models import DocumentItemProduct
from sale.tests.models.test_product import fake_product


def fake_document_item_product() -> DocumentItemProduct:
    """Create a fake document item product."""
    product = fake_product()
    return DocumentItemProduct.objects.create(
        price=5.0, quantity=2, discount=0.1, item_group="Test Group", product=product
    )


class DocumentItemProductTest(TestCase):
    """Test cases for the DocumentItemProduct model."""

    def test_title_str(self) -> None:
        """Test the title_str property."""
        item = fake_document_item_product()
        self.assertEqual(item.product.name, item.title_str)

    def test_comment_str(self) -> None:
        """Test the comment_str property."""
        item = fake_document_item_product()
        self.assertEqual(item.product.description, item.comment_str)
