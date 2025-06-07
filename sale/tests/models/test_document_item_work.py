"""Test cases for the DocumentItemWork model."""

from django.test import TestCase

from sale.models import DocumentItemWork
from sale.tests.models.test_work_type import fake_work_type


def fake_document_item_work() -> DocumentItemWork:
    """Create a fake document item work."""
    work_type = fake_work_type()
    return DocumentItemWork.objects.create(price=5.0, quantity=2, discount=0.1, work=work_type, comment="Test Comment")


class DocumentItemProductTest(TestCase):
    """Test cases for the DocumentItemProduct model."""

    def test_title_str(self) -> None:
        """Test the title_str property."""
        item = fake_document_item_work()
        self.assertEqual(item.work.name, item.title_str)

    def test_comment_str(self) -> None:
        """Test the comment_str property."""
        item = fake_document_item_work()
        self.assertEqual("Test Comment", item.comment_str)
