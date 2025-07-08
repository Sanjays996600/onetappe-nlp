import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from routes.invoices import generate_invoice_pdf
import io
import PyPDF2

class TestInvoiceGeneration(unittest.TestCase):
    def test_discount_calculation_percentage(self):
        """Test that percentage discounts are correctly applied to the subtotal before tax"""
        # Mock data
        order_data = {
            "id": 123,
            "items": [
                {
                    "product": "Test Product",
                    "quantity": 2,
                    "price": 100.00
                }
            ],
            "tax_rate": 10,
            "discount_percent": 20,
            "discount_amount": 0
        }
        
        seller_info = {
            "name": "Test Seller",
            "email": "seller@example.com"
        }
        
        customer_info = {
            "name": "Test Customer",
            "email": "customer@example.com"
        }
        
        # Generate PDF
        pdf_data = generate_invoice_pdf(order_data, seller_info, customer_info)
        
        # Expected calculations:
        # Subtotal: 2 * 100 = 200
        # Discount (20%): 200 * 0.2 = 40
        # Discounted subtotal: 200 - 40 = 160
        # Tax (10%): 160 * 0.1 = 16
        # Total: 160 + 16 = 176
        
        # Extract text from PDF to verify calculations
        pdf_file = io.BytesIO(pdf_data)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Check that the calculations are correct
        self.assertIn("Subtotal: $200.00", text)
        self.assertIn("Discount (20%): -$40.00", text)
        self.assertIn("Tax (10%): $16.00", text)
        self.assertIn("Total: $176.00", text)
    
    def test_discount_calculation_fixed_amount(self):
        """Test that fixed amount discounts are correctly applied to the subtotal before tax"""
        # Mock data
        order_data = {
            "id": 123,
            "items": [
                {
                    "product": "Test Product",
                    "quantity": 2,
                    "price": 100.00
                }
            ],
            "tax_rate": 10,
            "discount_percent": 0,
            "discount_amount": 50
        }
        
        seller_info = {
            "name": "Test Seller",
            "email": "seller@example.com"
        }
        
        customer_info = {
            "name": "Test Customer",
            "email": "customer@example.com"
        }
        
        # Generate PDF
        pdf_data = generate_invoice_pdf(order_data, seller_info, customer_info)
        
        # Expected calculations:
        # Subtotal: 2 * 100 = 200
        # Discount (fixed): 50
        # Discounted subtotal: 200 - 50 = 150
        # Tax (10%): 150 * 0.1 = 15
        # Total: 150 + 15 = 165
        
        # Extract text from PDF to verify calculations
        pdf_file = io.BytesIO(pdf_data)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Check that the calculations are correct
        self.assertIn("Subtotal: $200.00", text)
        self.assertIn("Discount: -$50.00", text)
        self.assertIn("Tax (10%): $15.00", text)
        self.assertIn("Total: $165.00", text)

if __name__ == "__main__":
    unittest.main()