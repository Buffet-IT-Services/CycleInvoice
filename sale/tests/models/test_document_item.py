"""Test cases for the DocumentItem model."""
from django.core.exceptions import ValidationError
from django.test import TestCase

from sale.models import DocumentItem


def fake_document_item_product() -> DocumentItem:
    """Create a fake document item for a product."""
    from sale.tests.models.test_product import fake_product
    product = fake_product()
    from contact.tests.models.test_contact import fake_contact
    return DocumentItem.objects.create(item_type="product", price=product.price, quantity=1, discount=0.1,
                                       customer=fake_contact(), product=product)


def fake_document_item_subscription() -> DocumentItem:
    """Create a fake document item for a subscription."""
    from sale.tests.models.test_subscription import fake_subscription
    subscription = fake_subscription()
    from contact.tests.models.test_contact import fake_contact
    return DocumentItem.objects.create(item_type="subscription", price=subscription.product.price, quantity=1,
                                       customer=fake_contact(), subscription=subscription,
                                       product=subscription.product.product, comment_title="Time Range")


def fake_document_item_work() -> DocumentItem:
    """Create a fake document item for a work."""
    from sale.tests.models.test_work_type import fake_work_type
    work = fake_work_type()
    from contact.tests.models.test_contact import fake_contact
    return DocumentItem.objects.create(price=work.price_per_hour, quantity=2.00, customer=fake_contact(),
                                       item_type="work", discount=0.1, comment_title="Test Date", work_type=work,
                                       comment_description="Test Description")


def fake_document_item_vehicle() -> DocumentItem:
    """Create a fake document item for a vehicle."""
    from vehicle.tests.models.test_vehicle import fake_vehicle
    vehicle = fake_vehicle()
    from contact.tests.models.test_contact import fake_contact
    return DocumentItem.objects.create(item_type="expense_vehicle", price=vehicle.km_sell, quantity=10,
                                       customer=fake_contact(), vehicle=vehicle, comment_title="10 km",
                                       comment_description="Oberrieden - Zürich")


class DocumentItemTest(TestCase):
    """Test cases for the DocumentItem model."""

    # noinspection DuplicatedCode
    def test_clean_product(self) -> None:
        """Test the clean method for a product item."""
        document_item = fake_document_item_product()

        document_item.product = None
        with self.assertRaises(ValidationError):
            document_item.clean()
        from sale.tests.models.test_product import fake_product
        document_item.product = fake_product()

        from sale.tests.models.test_subscription import fake_subscription
        document_item.subscription = fake_subscription()
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.subscription = None

        document_item.comment_title = "Test"
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.comment_title = None

        document_item.comment_description = "Test"
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.comment_description = None

        from vehicle.tests.models.test_vehicle import fake_vehicle
        document_item.vehicle = fake_vehicle()
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.vehicle = None

        from sale.tests.models.test_work_type import fake_work_type
        document_item.work_type = fake_work_type()
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.work_type = None

    # noinspection DuplicatedCode
    def test_clean_subscription(self) -> None:
        """Test the clean method for a subscription item."""
        document_item = fake_document_item_subscription()

        document_item.product = None
        with self.assertRaises(ValidationError):
            document_item.clean()
        from sale.tests.models.test_product import fake_product
        document_item.product = fake_product()

        from sale.tests.models.test_subscription import fake_subscription
        document_item.subscription = None
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.subscription = fake_subscription()

        document_item.comment_title = None
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.comment_title = "Test"

        document_item.comment_description = "Test"
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.comment_description = None

        from vehicle.tests.models.test_vehicle import fake_vehicle
        document_item.vehicle = fake_vehicle()
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.vehicle = None

        from sale.tests.models.test_work_type import fake_work_type
        document_item.work_type = fake_work_type()
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.work_type = None

    # noinspection DuplicatedCode
    def test_clean_work(self) -> None:
        """Test the clean method for a work item."""
        document_item = fake_document_item_work()

        from sale.tests.models.test_product import fake_product
        document_item.product = fake_product()
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.product = None

        from sale.tests.models.test_subscription import fake_subscription
        document_item.subscription = fake_subscription()
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.subscription = None

        document_item.comment_title = None
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.comment_title = "Test"

        document_item.comment_description = None
        try:
            document_item.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly when comment_description is None")

        from vehicle.tests.models.test_vehicle import fake_vehicle
        document_item.vehicle = fake_vehicle()
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.vehicle = None

        from sale.tests.models.test_work_type import fake_work_type
        document_item.work_type = None
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.work_type = fake_work_type()

    # noinspection DuplicatedCode
    def test_clean_expense_vehicle(self) -> None:
        """Test the clean method for a vehicle expense item."""
        document_item = fake_document_item_vehicle()

        from sale.tests.models.test_product import fake_product
        document_item.product = fake_product()
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.product = None

        from sale.tests.models.test_subscription import fake_subscription
        document_item.subscription = fake_subscription()
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.subscription = None

        document_item.comment_title = None
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.comment_title = "Test"

        document_item.comment_description = None
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.comment_description = "Test"

        from vehicle.tests.models.test_vehicle import fake_vehicle
        document_item.vehicle = None
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.vehicle = fake_vehicle()

        from sale.tests.models.test_work_type import fake_work_type
        document_item.work_type = fake_work_type()
        with self.assertRaises(ValidationError):
            document_item.clean()
        document_item.work_type = None

    def test_clean_invalid_item_type(self) -> None:
        """Test that ValueError is raised for an invalid item_type in clean property."""
        document_item = fake_document_item_product()
        document_item.item_type = "invalid_type"
        with self.assertRaises(ValidationError):
            document_item.clean()

    def test_property_price_str(self) -> None:
        """Test the price_str property."""
        self.assertEqual("100.00", fake_document_item_work().price_str)

    def test_property_quantity_str(self) -> None:
        """Test the quantity_str property."""
        document_item = fake_document_item_work()
        self.assertEqual("2", document_item.quantity_str)

        document_item.quantity = 2.22
        self.assertEqual("2.22", document_item.quantity_str)

    def test_property_total(self) -> None:
        """Test the total property."""
        document_item = fake_document_item_work()
        self.assertEqual(180.00, document_item.total)

        document_item.price = 0.01
        self.assertEqual(0.02, document_item.total)

    def test_property_total_str(self) -> None:
        """Test the total_str property."""
        document_item = fake_document_item_product()
        self.assertEqual("9.00", document_item.total_str)

    def test_property_discount_str(self) -> None:
        """Test the discount_str property."""
        document_item = fake_document_item_product()
        self.assertEqual("10.00%", document_item.discount_str)

        document_item.discount = 0
        self.assertEqual("", document_item.discount_str)

    def test_title_product(self) -> None:
        """Test the title property for a product."""
        document_item = fake_document_item_product()
        self.assertEqual("Test Product", document_item.title)

    def test_title_subscription(self) -> None:
        """Test the title property for a subscription."""
        document_item = fake_document_item_subscription()
        self.assertEqual("Test Product (Time Range)", document_item.title)

    def test_title_work(self) -> None:
        """Test the title property for a work."""
        document_item = fake_document_item_work()
        self.assertEqual("Test Work Type (Test Date)", document_item.title)

    def test_title_expense_vehicle(self) -> None:
        """Test the title property for a vehicle expense."""
        document_item = fake_document_item_vehicle()
        self.assertEqual("Kilometerspesen (10 km)", document_item.title)

    def test_title_invalid_item_type(self) -> None:
        """Test that ValueError is raised for an invalid item_type in title property."""
        document_item = fake_document_item_product()
        document_item.item_type = "invalid_type"
        with self.assertRaises(ValueError) as context:
            _ = document_item.title
        self.assertIn("Invalid item type: invalid_type", str(context.exception))

    def test_description_product(self) -> None:
        """Test the description property for a product."""
        document_item = fake_document_item_product()
        self.assertEqual("This is a test description.", document_item.description)

    def test_description_subscription(self) -> None:
        """Test the description property for a subscription."""
        document_item = fake_document_item_subscription()
        self.assertEqual("This is a test description.", document_item.description)

    def test_description_work(self) -> None:
        """Test the description property for a work."""
        document_item = fake_document_item_work()
        self.assertEqual("Test Description", document_item.description)

    def test_description_expense_vehicle(self) -> None:
        """Test the description property for a vehicle expense."""
        document_item = fake_document_item_vehicle()
        self.assertEqual("Oberrieden - Zürich", document_item.description)

    def test_description_invalid_item_type(self) -> None:
        """Test that ValueError is raised for an invalid item_type in description property."""
        document_item = fake_document_item_product()
        document_item.item_type = "invalid_type"
        with self.assertRaises(ValueError) as context:
            _ = document_item.description
        self.assertIn("Invalid item type: invalid_type", str(context.exception))
