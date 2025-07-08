# Invoice Generation Feature

## Overview

This feature adds the ability to generate PDF invoices for orders with proper discount and tax calculations. It fixes the bug identified in the Manual QA Report where percentage discounts were incorrectly applied after tax instead of before tax.

## Files Added/Modified

### Backend

1. **`routes/invoices.py`**: New module that provides API endpoints for generating invoices with proper discount calculation.

2. **`backend/main.py`**: Updated to include the new invoice routes in the FastAPI application.

3. **`tests/test_invoices.py`**: Unit tests that verify the correct calculation of both percentage and fixed amount discounts.

4. **`docs/invoice_generation.md`**: Documentation explaining the invoice generation functionality, API endpoints, and the discount calculation logic.

### Frontend

1. **`frontend/src/components/InvoiceGenerator.jsx`**: React component for generating invoices with or without discounts.

2. **`frontend/src/pages/seller-dashboard/InvoicePage.jsx`**: Page component that integrates the InvoiceGenerator.

3. **`frontend/src/pages/seller-dashboard/Orders.jsx`**: Updated to include a link to generate invoices for each order.

4. **`frontend/src/App.js`**: Updated to include the new InvoicePage route.

## Key Features

- **Proper Discount Calculation**: Fixed the bug where percentage discounts were incorrectly applied after tax. Now discounts are properly applied to the subtotal before calculating tax.

- **Flexible Discount Types**: Support for both percentage and fixed amount discounts.

- **API Endpoints**: 
  - `/seller/invoices/{order_id}` - Generate invoice without discount
  - `/seller/invoices/{order_id}/with-discount` - Generate invoice with specified discount

- **PDF Generation**: Professional-looking invoices with proper formatting and calculations.

- **Frontend Integration**: Easy-to-use UI for generating invoices with or without discounts.

## How to Test

### Backend Tests

Run the unit tests to verify the correct calculation of discounts and taxes:

```bash
python3 -m unittest tests.test_invoices
```

### Manual Testing

1. Start the backend and frontend servers.

2. Navigate to the Orders page in the seller dashboard.

3. Click on the "Generate Invoice" button for any order.

4. On the Invoice Generator page:
   - Click "Generate Standard Invoice" to create an invoice without discounts.
   - Or, select a discount type (percentage or fixed amount), enter a value, and click "Generate Invoice with Discount".

5. Verify that the generated PDF shows the correct calculations:
   - For percentage discounts, the discount should be applied to the subtotal before tax.
   - For fixed amount discounts, the discount should be applied to the subtotal before tax.
   - The tax should be calculated on the discounted subtotal.

## Dependencies

- ReportLab: Used for PDF generation
- PyPDF2: Used in tests to extract text from generated PDFs
- FastAPI: Used for API endpoints
- SQLAlchemy: Used for database access
- React: Used for frontend components