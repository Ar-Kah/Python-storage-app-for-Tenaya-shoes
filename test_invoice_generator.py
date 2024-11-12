import unittest
import os
from PyPDF2 import PdfReader  # Ensure PyPDF2 is installed
from invoice_generator import InvoiceGenerator  # assuming your code is in a file named invoice_generator.py


class TestInvoiceGenerator(unittest.TestCase):

    def setUp(self):
        # Sample test data for items
        self.items = [
            {"quantity": 10, "unit": "kg", "description": "Mansikkaa", "unit_price": 10.00},
            {"quantity": 20, "unit": "l", "description": "Mustikkaa", "unit_price": 5.59},
            {"quantity": 1, "unit": "kpl", "description": "Toimitusmaksu", "unit_price": 15.00},
        ]
        # Expected total (including tax)
        self.expected_total = sum(
            (item["quantity"] * item["unit_price"] * 1.24) for item in self.items
        )

        # Create an instance of InvoiceGenerator with the test data
        self.generator = InvoiceGenerator(self.items, output_file="test_invoice.pdf")

    def test_total_calculation(self):
        # Generate the PDF
        self.generator.generate()
        # Check if the calculated total matches the expected value
        self.assertAlmostEqual(self.generator.total, self.expected_total, places=2)

    def test_pdf_creation(self):
        # Generate the PDF
        self.generator.generate()

        # Check if the file exists
        self.assertTrue(os.path.exists("test_invoice.pdf"))

        # Check if the file is not empty
        file_size = os.path.getsize("test_invoice.pdf")
        self.assertTrue(file_size > 0, "The PDF file is empty")

    def test_pdf_content(self):
        # Generate the PDF and load it into a BytesIO object for in-memory reading
        self.generator.generate()

        # Read the content of the PDF with PdfReader
        with open("test_invoice.pdf", "rb") as f:
            pdf_reader = PdfReader(f)
            # Check that at least one page exists
            self.assertGreaterEqual(len(pdf_reader.pages), 1)

            # Extract text from the first page
            first_page_text = pdf_reader.pages[0].extract_text()
            # Check if essential content appears in the text, e.g., title and total amount
            self.assertIn("LASKU", first_page_text)  # Check if the title is present
            self.assertIn("Yhteensä EUR:", first_page_text)  # Check if total label is present
            self.assertIn(f"{self.generator.total:.2f}", first_page_text)  # Check if total amount is correct

    def tearDown(self):
        # Clean up the generated test file after each test
        if os.path.exists("test_invoice.pdf"):
            os.remove("test_invoice.pdf")


if __name__ == "__main__":
    unittest.main()
