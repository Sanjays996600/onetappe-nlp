# Invoice Generation Module

## Overview

The Invoice Generation module provides functionality to create PDF invoices for orders with proper discount and tax calculations. This module was created to fix the bug identified in the Manual QA Report where percentage discounts were incorrectly applied after tax instead of before tax.

## Key Features

- Generate PDF invoices for any order in the system
- Apply discounts (percentage or fixed amount) correctly to the subtotal before calculating tax
- Properly format invoice with seller and customer information
- Include itemized order details with proper calculations

## API Endpoints

### Get Invoice for Order

```
GET /seller/invoices/{order_id}
```

Generates a PDF invoice for the specified order without any discount.

### Get Invoice with Discount

```
GET /seller/invoices/{order_id}/with-discount?discount_type=percent&discount_value=10
```

Generates a PDF invoice for the specified order with a discount applied. The discount can be either a percentage or a fixed amount.

**Query Parameters:**

- `discount_type`: Type of discount, either "percent" or "amount" (default: "percent")
- `discount_value`: Value of the discount, either a percentage or a fixed amount (default: 0)

## Discount Calculation Logic

The module implements the correct discount calculation logic:

1. Calculate the subtotal of all items in the order
2. Apply any discounts (percentage or fixed amount) to the subtotal
3. Calculate tax based on the discounted subtotal
4. Calculate the total by adding the tax to the discounted subtotal

This ensures that percentage discounts are correctly applied to the subtotal before tax, fixing the bug identified in the Manual QA Report.

## Testing

The module includes unit tests to verify the correct calculation of discounts and taxes. The tests check both percentage and fixed amount discounts to ensure they are applied correctly.

To run the tests:

```bash
python -m unittest tests/test_invoices.py
```

## Dependencies

- ReportLab: Used for PDF generation
- PyPDF2: Used in tests to extract text from generated PDFs
- FastAPI: Used for API endpoints
- SQLAlchemy: Used for database access