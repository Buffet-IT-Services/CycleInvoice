"""Test cases for the DocumentItemWork model."""

from django.test import TestCase

from sale.models import DocumentItemWork
from sale.tests.models.test_work_type_price import fake_work_type_price


def fake_document_item_work() -> DocumentItemWork:
    """Create a fake document item work."""
    work_type_price = fake_work_type_price()
    return DocumentItemWork.objects.create(
        price=5.0, quantity=2, discount=0.1, item_group="Test Group", work=work_type_price, comment="Test Comment"
    )


class DocumentItemProductTest(TestCase):
    """Test cases for the DocumentItemProduct model."""

    def test_title_str(self) -> None:
        """Test the title_str property."""
        item = fake_document_item_work()
        self.assertEqual(item.work.work_type.name, item.title_str)

    def test_comment_str(self) -> None:
        """Test the comment_str property."""
        item = fake_document_item_work()
        self.assertEqual("Test Comment", item.comment_str)
