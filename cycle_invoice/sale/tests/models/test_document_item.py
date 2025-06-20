"""Test cases for the DocumentItem model."""
from django.core.exceptions import ValidationError
from django.test import TestCase

from cycle_invoice.common.tests.base import get_default_test_user
from cycle_invoice.contact.tests.models.test_contact import fake_contact
from cycle_invoice.sale.models import DocumentItem
from cycle_invoice.product.tests.models.test_product import fake_product
from cycle_invoice.subscription.tests.models.test_subscription import fake_subscription
from cycle_invoice.work.test.models.test_work_type import fake_work_type
from cycle_invoice.vehicle.tests.models.test_vehicle import fake_vehicle


def fake_document_item_product(save: bool) -> DocumentItem:  # noqa: FBT001
    """Create a fake document item for a product."""
    product = fake_product(save=True)
    document_item = DocumentItem(
        item_type="product",
        price=product.price,
        quantity=1,
        discount=0.1,
        customer=fake_contact(save=True),
        product=product,
    )
    if save:
        document_item.save(user=get_default_test_user())
    return document_item


def fake_document_item_subscription(save: bool) -> DocumentItem:  # noqa: FBT001
    """Create a fake document item for a subscription."""
    subscription = fake_subscription(save=True)
    document_item = DocumentItem(
        item_type="subscription",
        price=subscription.product.price,
        quantity=1,
        customer=fake_contact(save=True),
        subscription=subscription,
        product=subscription.product.product,
        comment_title="Time Range"
    )
    if save:
        document_item.save(user=get_default_test_user())
    return document_item


def fake_document_item_work(save: bool) -> DocumentItem:  # noqa: FBT001
    """Create a fake document item for a work."""
    work = fake_work_type(save=True)
    document_item = DocumentItem(
        price=work.price_per_hour,
        quantity=2.00,
        customer=fake_contact(save=True),
        item_type="work",
        discount=0.1,
        comment_title="Test Date",
        work_type=work,
        comment_description="Test Description"
    )
    if save:
        document_item.save(user=get_default_test_user())
    return document_item


def fake_document_item_vehicle() -> DocumentItem:
    """Create a fake document item for a vehicle."""
    vehicle = fake_vehicle(save=True)
    return DocumentItem(
        item_type="expense_vehicle",
        price=vehicle.km_sell,
        quantity=10,
        customer=fake_contact(save=True),
        vehicle=vehicle,
        comment_title="10 km",
        comment_description="Oberrieden - Zürich"
    )


class DocumentItemTest(TestCase):
    """Test cases for the DocumentItem model."""

    def setUp(self) -> None:
        """Set up test data for DocumentItem tests."""
        self.vehicle = fake_vehicle(save=True)
        self.product = fake_product(save=True)
        self.subscription = fake_subscription(save=True)
        self.work_type = fake_work_type(save=True)

    # noinspection DuplicatedCode
    def test_clean_product(self) -> None:
        """Test the clean method for a product item."""
        document_item = fake_document_item_product(save=True)

        document_item.product = None
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.product = self.product

        document_item.subscription = self.subscription
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.subscription = None

        document_item.comment_title = "Test"
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.comment_title = None

        document_item.comment_description = "Test"
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.comment_description = None

        document_item.vehicle = self.vehicle
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.vehicle = None

        document_item.work_type = self.work_type
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.work_type = None

    # noinspection DuplicatedCode
    def test_clean_subscription(self) -> None:
        """Test the clean method for a subscription item."""
        document_item = fake_document_item_subscription(save=False)

        document_item.product = None
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.product = self.product

        document_item.subscription = None
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.subscription = self.subscription

        document_item.comment_title = None
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.comment_title = "Test"

        document_item.comment_description = "Test"
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.comment_description = None

        document_item.vehicle = self.vehicle
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.vehicle = None

        document_item.work_type = self.work_type
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.work_type = None

    # noinspection DuplicatedCode
    def test_clean_work(self) -> None:
        """Test the clean method for a work item."""
        document_item = fake_document_item_work(save=False)

        document_item.product = self.product
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.product = None

        document_item.subscription = self.subscription
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.subscription = None

        document_item.comment_title = None
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.comment_title = "Test"

        document_item.comment_description = None
        try:
            document_item.validate_constraints()
        except ValidationError:
            self.fail("validate_constraints() raised ValidationError unexpectedly when comment_description is None")

        document_item.vehicle = self.vehicle
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.vehicle = None

        document_item.work_type = None
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.work_type = self.work_type

    # noinspection DuplicatedCode
    def test_clean_expense_vehicle(self) -> None:
        """Test the clean method for a vehicle expense item."""
        document_item = fake_document_item_vehicle()

        document_item.product = self.product
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.product = None

        document_item.subscription = self.subscription
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.subscription = None

        document_item.comment_title = None
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.comment_title = "Test"

        document_item.comment_description = None
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.comment_description = "Test"

        document_item.vehicle = None
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.vehicle = self.vehicle

        document_item.work_type = self.work_type
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()
        document_item.work_type = None

    def test_clean_invalid_item_type(self) -> None:
        """Test that ValueError is raised for an invalid item_type in clean property."""
        document_item = fake_document_item_product(save=False)
        document_item.item_type = "invalid_type"
        with self.assertRaises(ValidationError):
            document_item.validate_constraints()

    def test_property_price_str(self) -> None:
        """Test the price_str property."""
        self.assertEqual("100.00", fake_document_item_work(save=False).price_str)

    def test_property_quantity_str(self) -> None:
        """Test the quantity_str property."""
        document_item = fake_document_item_work(save=False)
        self.assertEqual("2", document_item.quantity_str)

        document_item.quantity = 2.22
        self.assertEqual("2.22", document_item.quantity_str)

    def test_property_total(self) -> None:
        """Test the total property."""
        document_item = fake_document_item_work(save=False)
        self.assertEqual(180.00, document_item.total)

        document_item.price = 0.01
        self.assertEqual(0.02, document_item.total)

    def test_property_total_str(self) -> None:
        """Test the total_str property."""
        self.assertEqual("9.00", fake_document_item_product(save=False).total_str)

    def test_property_discount_str(self) -> None:
        """Test the discount_str property."""
        document_item = fake_document_item_product(save=False)
        self.assertEqual("10.00%", document_item.discount_str)

        document_item.discount = 0
        self.assertEqual("", document_item.discount_str)

    def test_title_product(self) -> None:
        """Test the title property for a product."""
        self.assertEqual("Test Product", fake_document_item_product(save=False).title)

    def test_title_subscription(self) -> None:
        """Test the title property for a subscription."""
        self.assertEqual("Test Product (Time Range)", fake_document_item_subscription(save=False).title)

    def test_title_work(self) -> None:
        """Test the title property for a work."""
        self.assertEqual("Test Work Type (Test Date)", fake_document_item_work(save=False).title)

    def test_title_expense_vehicle(self) -> None:
        """Test the title property for a vehicle expense."""
        document_item = fake_document_item_vehicle()
        self.assertEqual("Kilometerspesen (10 km)", document_item.title)

    def test_title_invalid_item_type(self) -> None:
        """Test that ValueError is raised for an invalid item_type in title property."""
        document_item = fake_document_item_product(save=False)
        document_item.item_type = "invalid_type"
        with self.assertRaises(ValueError) as context:
            _ = document_item.title
        self.assertIn("Invalid item type: invalid_type", str(context.exception))

    def test_description_product(self) -> None:
        """Test the description property for a product."""
        self.assertEqual("This is a test description.", fake_document_item_product(save=False).description)

    def test_description_subscription(self) -> None:
        """Test the description property for a subscription."""
        self.assertEqual("This is a test description.", fake_document_item_subscription(save=False).description)

    def test_description_work(self) -> None:
        """Test the description property for a work."""
        self.assertEqual("Test Description", fake_document_item_work(save=False).description)

    def test_description_expense_vehicle(self) -> None:
        """Test the description property for a vehicle expense."""
        document_item = fake_document_item_vehicle()
        self.assertEqual("Oberrieden - Zürich", document_item.description)

    def test_description_invalid_item_type(self) -> None:
        """Test that ValueError is raised for an invalid item_type in description property."""
        document_item = fake_document_item_product(save=False)
        document_item.item_type = "invalid_type"
        with self.assertRaises(ValueError) as context:
            _ = document_item.description
        self.assertIn("Invalid item type: invalid_type", str(context.exception))
