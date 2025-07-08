# NLP Command System QA Testing Plan

## Overview

This document outlines the comprehensive testing strategy for the seller-side NLP command system, focusing on multilingual functionality (English & Hindi), end-to-end command processing, entity extraction, formatting, error handling, and WhatsApp-based input/output.

## Test Categories

### 1. Unit Tests

#### Intent Detection Tests
- Verify correct intent detection for all supported commands in both English and Hindi
- Test with various phrasings and sentence structures
- Ensure robustness against minor typos and grammatical errors

#### Entity Extraction Tests
- Verify extraction of numeric values (limits, thresholds)
- Test date and time range extraction
- Test product name and detail extraction
- Verify handling of special characters and Unicode

### 2. Integration Tests

#### Command Routing Tests
- Verify correct API endpoint selection based on intent
- Test parameter preparation and formatting
- Verify response formatting based on language

#### API Interaction Tests
- Test successful API responses
- Test error handling for various API error conditions
- Verify fallback to simulated responses when appropriate

### 3. WhatsApp Integration Tests

#### Message Handling Tests
- Test parsing of incoming WhatsApp messages
- Verify correct response generation and formatting
- Test handling of Unicode characters and emojis

#### Session Management Tests
- Test user session tracking
- Verify language preference persistence
- Test conversation flow with multiple messages

### 4. Edge Case Tests

#### Robustness Tests
- Test with empty or nonsensical input
- Test with extremely long commands
- Test with mixed language input
- Test with unusual number and date formats

#### Error Handling Tests
- Verify graceful handling of unknown intents
- Test recovery from parsing errors
- Verify appropriate error messages in both languages

## Test Execution Plan

### Automated Tests

Run the following test suites:

```bash
python -m nlp.run_tests
python -m nlp.test_edge_cases
python -m nlp.test_get_customer_data
python -m nlp.test_get_top_products
python -m nlp.test_get_low_stock
python -m nlp.test_search_product
python -m nlp.test_whatsapp_integration
python -m nlp.test_whatsapp_parser
```

### Manual Tests

Execute the following manual tests to verify end-to-end functionality:

#### English Commands

```bash
python -c "from nlp.multilingual_handler import parse_multilingual_command; print(parse_multilingual_command('Show my inventory'))"
python -c "from nlp.multilingual_handler import parse_multilingual_command; print(parse_multilingual_command('Show top 3 customers this week'))"
python -c "from nlp.multilingual_handler import parse_multilingual_command; print(parse_multilingual_command('Show low stock items below 10'))"
python -c "from nlp.multilingual_handler import parse_multilingual_command; print(parse_multilingual_command('Search for rice'))"
python -c "from nlp.multilingual_handler import parse_multilingual_command; print(parse_multilingual_command('Show sales report for last month'))"
```

#### Hindi Commands

```bash
python -c "from nlp.hindi_support import parse_hindi_command; print(parse_hindi_command('मेरा इन्वेंटरी दिखाओ'))"
python -c "from nlp.hindi_support import parse_hindi_command; print(parse_hindi_command('इस हफ्ते के टॉप 3 ग्राहक दिखाओ'))"
python -c "from nlp.hindi_support import parse_hindi_command; print(parse_hindi_command('10 से कम स्टॉक वाले आइटम दिखाओ'))"
python -c "from nlp.hindi_support import parse_hindi_command; print(parse_hindi_command('चावल सर्च करो'))"
python -c "from nlp.hindi_support import parse_hindi_command; print(parse_hindi_command('पिछले महीने का सेल्स रिपोर्ट दिखाओ'))"
```

## QA Testing Sheet Structure

Document test results in a structured format with the following columns:

| Intent | Language | Test Input | Expected Output | Actual Output | Status | Bug ID |
|--------|----------|------------|-----------------|---------------|--------|--------|
| get_inventory | en | Show my inventory | List of products with stock and prices | [Actual response] | Pass/Fail | [If applicable] |

## WhatsApp Testing Checklist

Once WhatsApp API gateway is integrated, verify:

- [ ] Command triggers via WhatsApp chat work correctly
- [ ] Hindi/Unicode text is properly encoded and decoded
- [ ] Response formatting is appropriate for WhatsApp
- [ ] Images and rich media are displayed correctly
- [ ] Error messages are user-friendly
- [ ] Session persistence works across multiple messages

## Bug Severity Classification

Classify bugs according to the following severity levels:

- **Critical**: System crash, data loss, security vulnerability
- **High**: Major functionality broken, no workaround available
- **Medium**: Feature partially working, workaround available
- **Low**: Minor issues, cosmetic problems, rare edge cases

## Completion Criteria

The QA milestone will be considered complete when:

- All automated tests pass in both English & Hindi
- NLP performs accurately across edge and fallback scenarios
- WhatsApp NLP flow works end-to-end
- No critical or high-priority bugs remain open

## Reporting

Send daily updates to Sanjay by 9 PM IST covering:
- What was tested
- Any issues found
- Pending verifications

## Appendix: Common Test Commands

### get_inventory
- Show my inventory
- मेरा इन्वेंटरी दिखाओ

### get_customer_data
- Show top 5 customers
- टॉप 5 ग्राहक दिखाओ

### get_top_products
- Show top 3 products this week
- इस हफ्ते के टॉप 3 प्रोडक्ट्स बताओ

### get_low_stock
- Show low stock items
- कम स्टॉक वाले आइटम दिखाओ

### search_product
- Search for rice
- चावल सर्च करो

### get_report
- Show sales report for last month
- पिछले महीने का सेल्स रिपोर्ट दिखाओ

### get_orders
- Show my recent orders
- मेरे हाल के ऑर्डर दिखाओ