import unittest
import os
import sys
import tempfile
import json
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the module to test
from routes.inventory import generate_inventory_pdf_report

class TestInventoryReportPDF(unittest.TestCase):
    """Test cases for inventory report PDF generation"""
    
    def setUp(self):
        """Set up test data"""
        # Sample inventory data for testing
        self.test_products = [
            {
                "id": "1",
                "name": "Test Product 1",
                "price": 100.0,
                "stock": 50,
                "category": "Test Category",
                "low_stock_threshold": 10
            },
            {
                "id": "2",
                "name": "Test Product 2",
                "price": 200.0,
                "stock": 5,
                "category": "Test Category",
                "low_stock_threshold": 10
            },
            {
                "id": "3",
                "name": "Test Product 3",
                "price": 300.0,
                "stock": 0,
                "category": "Another Category",
                "low_stock_threshold": 5
            }
        ]
        
        # Sample seller data
        self.seller_info = {
            "id": "seller123",
            "name": "Test Seller",
            "business_name": "Test Business",
            "phone": "+919876543210"
        }
    
    def test_pdf_generation(self):
        """Test that PDF is generated with correct content"""
        # Create a temporary file to save the PDF
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Generate the PDF
            pdf_path = generate_inventory_pdf_report(self.test_products, self.seller_info)
            
            # Check that the PDF was created
            self.assertTrue(os.path.exists(pdf_path), "PDF file was not created")
            
            # Check the file size is reasonable (not empty)
            file_size = os.path.getsize(pdf_path)
            self.assertGreater(file_size, 1000, "PDF file is too small, might be empty")
            
            # Note: For a more thorough test, we would need to parse the PDF content
            # and verify specific text elements, but that requires additional libraries
            print(f"PDF generated successfully at {pdf_path} with size {file_size} bytes")
            
        finally:
            # Clean up - remove the temporary file
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_pdf_with_empty_inventory(self):
        """Test PDF generation with empty inventory"""
        # Generate PDF with empty product list
        pdf_path = generate_inventory_pdf_report([], self.seller_info)
        
        # Check that the PDF was created despite empty inventory
        self.assertTrue(os.path.exists(pdf_path), "PDF file was not created for empty inventory")
        
        # Clean up
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)
    
    def test_pdf_content_structure(self):
        """Test the structure of the PDF content"""
        # This is a placeholder for a more advanced test that would
        # parse the PDF content and verify specific elements
        
        # For manual testing, print the expected content structure
        print("\nExpected PDF content structure:")
        print("1. Header with seller information")
        print("2. Title: Inventory Report")
        print("3. Date and time of generation")
        print("4. Summary statistics:")
        print("   - Total products: 3")
        print("   - Total stock: 55")
        print("   - Low stock items: 1")
        print("   - Out of stock items: 1")
        print("5. Product table with columns:")
        print("   - ID")
        print("   - Name")
        print("   - Category")
        print("   - Price")
        print("   - Stock")
        print("   - Status (Normal/Low/Out of Stock)")
        
        # For a complete test, we would need to extract text from the PDF
        # and verify these elements are present

if __name__ == "__main__":
    unittest.main()