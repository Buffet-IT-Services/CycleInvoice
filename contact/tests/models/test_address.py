"""Test cases for the Address model."""

from django.test import TestCase

from contact.models import Address, address_block


def fake_address() -> Address:
    """Create a fake address."""
    return Address.objects.create(street="Main St", number="1", city="Any town", zip_code="1234", country="Switzerland")


def fake_address_with_additional() -> Address:
    """Create a fake address with additional info."""
    return Address.objects.create(
        street="Main St",
        number="1",
        additional="c/o Company",
        city="Any town",
        zip_code="1234",
        country="Switzerland",
    )


class AddressTest(TestCase):
    """Test cases for the Address model."""

    def test_str(self) -> None:
        """Test the __str__ of Address."""
        address = fake_address_with_additional()
        self.assertEqual("c/o Company, Main St 1, 1234 Any town, Switzerland", str(address))

        address = fake_address()
        self.assertEqual("Main St 1, 1234 Any town, Switzerland", str(address))

    def test_address_block(self) -> None:
        """Test the address block function."""
        address = fake_address_with_additional()
        self.assertEqual("c/o Company\nMain St 1\n1234 Any town\nSwitzerland", address_block(address))

        address = fake_address()
        self.assertEqual("Main St 1\n1234 Any town\nSwitzerland", address_block(address))

    def test_save_address_not_referenced(self) -> None:
        """Test saving an address that is not referenced."""
        addr = fake_address()
        addr.street = "B"
        addr.save()
        self.assertEqual(addr.street, "B")
        self.assertFalse(addr.disabled)

    def test_save_address_referenced_creates_new(self) -> None:
        """Test saving an address that is referenced by DocumentItemKilometers."""
        from vehicle.tests.models.test_document_item_kilometers import fake_document_item_kilometers
        inv_item = fake_document_item_kilometers()

        # Make changes to the address
        addr = Address.objects.get(pk=inv_item.start_address.pk)
        addr.street = "B"
        addr.save()

        inv_item.refresh_from_db()

        # The old address should be disabled
        old_addr = Address.objects.get(pk=inv_item.start_address.pk)
        self.assertTrue(old_addr.disabled)

        # The new address should exist and not be disabled
        new_addr = Address.objects.get(street="B")
        self.assertFalse(new_addr.disabled)

        # DocumentItemKilometers should still point to the old address
        self.assertEqual(inv_item.start_address.pk, old_addr.pk)

    def test_save_address_referenced_by_customer_updates_customer(self) -> None:
        """Test saving an address that is referenced by a Customer."""
        from contact.models import Address, Customer
        from vehicle.tests.models.test_document_item_kilometers import fake_document_item_kilometers
        inv_item = fake_document_item_kilometers()
        customer = Customer.objects.get(pk=inv_item.customer.pk)
        customer.address = inv_item.start_address
        customer.save()

        # Make changes to the address
        addr = Address.objects.get(pk=inv_item.start_address.pk)
        addr.street = "B"
        addr.save()

        inv_item.refresh_from_db()

        # The old address should be disabled
        old_addr = Address.objects.get(pk=inv_item.start_address.pk)
        self.assertTrue(old_addr.disabled)

        # The new address should exist and not be disabled
        new_addr = Address.objects.get(street="B")
        self.assertFalse(new_addr.disabled)

        # Customer should now point to the new address
        customer.refresh_from_db()
        self.assertEqual(customer.address.pk, new_addr.pk)

    def test_save_address_only_additional_changes(self) -> None:
        """Test saving an address with only additional info changed."""
        from vehicle.tests.models.test_document_item_kilometers import fake_document_item_kilometers
        inv_item = fake_document_item_kilometers()

        # Make changes to the address
        addr = Address.objects.get(pk=inv_item.start_address.pk)
        addr.additional = "bar"
        addr.save()
        addr.refresh_from_db()

        # The address should not be disabled
        self.assertEqual(addr.additional, "bar")
        self.assertFalse(addr.disabled)
