# Inventory Report Testing Guide

## Overview

This guide provides instructions for testing the inventory report functionality in OneTappe. The inventory report feature allows sellers to generate PDF reports of their current inventory status through both the WhatsApp chatbot interface and the seller dashboard.

## Test Files and Resources

### Test Plans and Checklists

1. **`inventory_report_test_plan.md`**
   - Comprehensive test plan covering WhatsApp interface, PDF generation, and dashboard integration
   - Includes detailed test cases with IDs, steps, and expected results

2. **`inventory_report_visual_checklist.md`**
   - Visual testing checklist for ensuring PDF report quality and consistency
   - Covers layout, formatting, language support, and device compatibility

3. **`inventory_report_test_results_template.md`**
   - Template for documenting test results
   - Includes sections for test summary, detailed results, and bug reporting

### Test Scripts

1. **`test_get_inventory_report.py`** (in `nlp` directory)
   - Tests the WhatsApp chatbot command recognition for inventory report requests
   - Verifies both English and Hindi command handling

2. **`test_inventory_report_pdf.py`** (in `routes` directory)
   - Tests the PDF generation functionality
   - Verifies content, structure, and handling of different inventory scenarios

3. **`inventory_report_test_data_generator.py`**
   - Generates test data with various inventory sizes and stock conditions
   - Creates JSON files that can be used for testing

4. **`run_inventory_report_tests.py`**
   - Helper script to run all tests and open relevant documents
   - Generates test data and creates test result files

## Testing Process

### Step 1: Prepare Test Environment

1. Ensure you have access to:
   - A test seller account with inventory data
   - WhatsApp test number for chatbot testing
   - Access to the seller dashboard

2. Generate test data (optional):
   ```
   python inventory_report_test_data_generator.py --size=medium --output=test_inventory.json
   ```
   Available sizes: small (10 products), medium (50 products), large (200 products), xlarge (1000 products)

### Step 2: Run Automated Tests

1. Run NLP command recognition tests:
   ```
   python ../nlp/test_get_inventory_report.py
   ```

2. Run PDF generation tests:
   ```
   python ../routes/test_inventory_report_pdf.py
   ```

3. Or use the helper script to run all tests:
   ```
   python run_inventory_report_tests.py --all
   ```

### Step 3: Perform Manual Testing

1. Open the test plan:
   ```
   python run_inventory_report_tests.py --open-plan
   ```

2. Create a new test results file:
   ```
   python run_inventory_report_tests.py --create-results
   ```

3. Follow the test cases in the test plan, documenting results in the test results file

4. For visual testing of PDFs, use the visual checklist:
   ```
   python run_inventory_report_tests.py --open-checklist
   ```

### Step 4: Test Across Devices and Languages

Ensure to test on multiple devices and browsers:

1. **Desktop**: Chrome, Firefox, Safari, Edge
2. **Mobile**: Android Chrome, iOS Safari
3. **Tablet**: iPad Safari, Android Chrome

Test in all supported languages:
1. English
2. Hindi
3. Hinglish (mixed Hindi-English)

### Step 5: Document and Report Issues

1. Complete the test results document with all findings
2. Report any bugs found using the bug report template in the test results document
3. Include screenshots of any visual issues
4. Submit the completed test results document to the QA lead

## Common Test Scenarios

### WhatsApp Command Testing

1. **Basic Commands**:
   - "inventory report"
   - "generate inventory report"
   - "इन्वेंटरी रिपोर्ट"
   - "इन्वेंटरी रिपोर्ट जनरेट करें"

2. **Error Scenarios**:
   - Testing with empty inventory
   - Testing with expired session
   - Testing during server maintenance

### PDF Report Testing

1. **Content Verification**:
   - Seller information correct
   - Summary statistics accurate
   - Product details complete and accurate
   - Status indicators (normal/low/out of stock) correct

2. **Format Testing**:
   - PDF opens in standard viewers
   - Layout consistent across devices
   - Text readable on all devices
   - Pagination works correctly for large inventories

### Dashboard Integration Testing

1. **Report Generation Flow**:
   - Report button visible and accessible
   - Loading indicator shown during generation
   - Download starts automatically
   - Report history updated

2. **Language Support**:
   - Interface elements correctly translated
   - PDF headers and content in selected language

## Contact Information

For questions or issues related to inventory report testing, please contact:

- QA Lead: [Name] ([Email])
- Developer: [Name] ([Email])

## Test Data Management

Test data files are stored in the `qa` directory. When generating large test data files, please add them to `.gitignore` to avoid committing large files to the repository.