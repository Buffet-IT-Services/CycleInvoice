"""Test cases for the Swiss QR utils."""
import hashlib

from django.test import TestCase

from cycle_invoice.sale.utils.swiss_qr import generate_qr_reference, generate_swiss_qr, modulo10_recursive


class SwissQRTest(TestCase):
    """Test cases for the Swiss QR utils."""

    def test_modulo10_recursive_basic(self) -> None:
        """Test the modulo10_recursive function with standard examples from the Swiss QR Standard Annex B and others."""
        self.assertEqual(modulo10_recursive("21000000000313947143000901"), "7")
        self.assertEqual(modulo10_recursive("00000000000000000000000000"), "0")
        self.assertEqual(modulo10_recursive("12345600010388500100001918"), "8")
        self.assertEqual(modulo10_recursive("21000000000313947143000901"), "7")
        self.assertEqual(modulo10_recursive("00000000000000000000012345"), "7")

    def test_generate_qr_reference_length_and_check(self) -> None:
        """Test that generate_qr_reference returns a reference of length 27 and that the check digit is correct."""
        for base in ["1", "123", "99999999999999999999999999", "12345"]:
            ref = generate_qr_reference(base)
        self.assertEqual(len(ref), 27)
        self.assertTrue(ref.__contains__(base))
        self.assertEqual(ref[-1], modulo10_recursive(ref[:-1]))

    def test_generate_swiss_qr(self) -> None:
        """Test the generate_swiss_qr function to ensure it adds a valid SVG QR bill to the context data."""
        context_data = {
            "company_info": {
                "company_bank_account": "CH4431999123000889012",
                "company_name": "Test AG",
                "company_address": "Teststrasse 1",
                "zip": "8000",
                "city": "Zürich",
                "country": "Schweiz",
            },
            "customer": {
                "name": "Max Mustermann",
                "street": "Musterweg 2",
                "postal_code": "4000",
                "city": "Basel",
                "country": "Schweiz",
            },
            "invoice_details": {
                "invoice_number": "2024-001",
                "invoice_primary_key": "12345",
                "total_sum": "123.45",
            },
        }
        result = generate_swiss_qr(context_data.copy())

        # Check if the result contains an SVG
        self.assertIn("qr_bill_svg", result)
        self.assertIsInstance(result["qr_bill_svg"], str)
        self.assertTrue(result["qr_bill_svg"].__contains__("<svg"))

        # Check if the SVG contains the expected information
        self.assertIn("CH44 3199 9123 0008 8901 2", result["qr_bill_svg"])
        self.assertIn("Test AG", result["qr_bill_svg"])
        self.assertIn("Teststrasse 1", result["qr_bill_svg"])
        self.assertIn("8000 Zürich", result["qr_bill_svg"])
        self.assertIn("Max Mustermann", result["qr_bill_svg"])
        self.assertIn("Musterweg 2", result["qr_bill_svg"])
        self.assertIn("4000 Basel", result["qr_bill_svg"])
        self.assertIn("123.45", result["qr_bill_svg"])
        self.assertIn("Rechnung 2024-001", result["qr_bill_svg"])
        self.assertIn("00 00000 00000 00000 00001 23457", result["qr_bill_svg"])

        # Check if the SVG hash matches the expected value
        hashed_result = hashlib.sha256(result["qr_bill_svg"].encode("utf-8")).hexdigest()
        self.assertEqual("77ddae4e783e2c358e4cef6026c02e78c6d7fa7887129af85acfab2af5d77d9a", hashed_result)