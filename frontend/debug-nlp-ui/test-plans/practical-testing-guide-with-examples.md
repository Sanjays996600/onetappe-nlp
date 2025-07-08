# Practical Testing Guide with Examples

## Overview

This document provides practical guidance for executing the multilingual WhatsApp chatbot tests, including specific examples with expected outcomes. It serves as a hands-on companion to the comprehensive test execution plan.

## Testing Environment Setup

### Accessing the Testing Interface

1. Open your web browser and navigate to http://localhost:3000
2. The interface should display a WhatsApp-like chat interface
3. Verify that you can type messages and receive responses

## Example Test Cases with Expected Outcomes

### Inventory Management Commands

#### English Examples

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "Show my inventory" | English | get_inventory | List of inventory items with quantities |
| "check stock" | English | get_inventory | List of inventory items with quantities |
| "Show low stock items" | English | get_low_stock | List of items below threshold quantity |
| "running out items" | English | get_low_stock | List of items below threshold quantity |
| "Update stock for XYZ to 50 units" | English | edit_stock | Confirmation of stock update for XYZ |
| "xyz stock 50" | English | edit_stock | Confirmation of stock update for XYZ |
| "Add new product XYZ with price 100 and quantity 25" | English | add_product | Confirmation of new product addition |
| "new prod xyz 100 25" | English | add_product | Confirmation of new product addition |

#### Hindi Examples (Devanagari)

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "मेरा इन्वेंटरी दिखाओ" | Hindi | get_inventory | List of inventory items with quantities in Hindi |
| "स्टॉक चेक करो" | Hindi | get_inventory | List of inventory items with quantities in Hindi |
| "कम स्टॉक वाले आइटम दिखाओ" | Hindi | get_low_stock | List of items below threshold quantity in Hindi |
| "खत्म हो रहे प्रोडक्ट" | Hindi | get_low_stock | List of items below threshold quantity in Hindi |
| "XYZ का स्टॉक 50 यूनिट अपडेट करो" | Hindi | edit_stock | Confirmation of stock update for XYZ in Hindi |
| "xyz स्टॉक 50" | Hindi | edit_stock | Confirmation of stock update for XYZ in Hindi |
| "नया प्रोडक्ट XYZ कीमत 100 और मात्रा 25 जोड़ें" | Hindi | add_product | Confirmation of new product addition in Hindi |
| "xyz नया 100 रुपये 25 पीस" | Hindi | add_product | Confirmation of new product addition in Hindi |

#### Hinglish Examples (Romanized Hindi)

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "Mera inventory dikhao" | Hinglish | get_inventory | List of inventory items with quantities |
| "Stock check karo" | Hinglish | get_inventory | List of inventory items with quantities |
| "Kam stock wale item dikhao" | Hinglish | get_low_stock | List of items below threshold quantity |
| "Khatam ho rahe product" | Hinglish | get_low_stock | List of items below threshold quantity |
| "XYZ ka stock 50 unit update karo" | Hinglish | edit_stock | Confirmation of stock update for XYZ |
| "xyz stock 50 kar do" | Hinglish | edit_stock | Confirmation of stock update for XYZ |
| "Naya product XYZ price 100 aur quantity 25 add karo" | Hinglish | add_product | Confirmation of new product addition |
| "xyz naya 100 rupaye 25 piece" | Hinglish | add_product | Confirmation of new product addition |

### Order Management Commands

#### English Examples

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "Show my recent orders" | English | get_orders | List of recent orders with basic details |
| "pending orders?" | English | get_orders | List of pending orders with basic details |
| "Show details for order #12345" | English | get_order_details | Detailed information about order #12345 |
| "12345 details" | English | get_order_details | Detailed information about order #12345 |
| "Mark order #12345 as delivered" | English | update_order_status | Confirmation of status update to delivered |
| "12345 delivered" | English | update_order_status | Confirmation of status update to delivered |

#### Hindi Examples (Devanagari)

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "मेरे हाल के ऑर्डर दिखाओ" | Hindi | get_orders | List of recent orders with basic details in Hindi |
| "बाकी ऑर्डर?" | Hindi | get_orders | List of pending orders with basic details in Hindi |
| "ऑर्डर #12345 का विवरण दिखाओ" | Hindi | get_order_details | Detailed information about order #12345 in Hindi |
| "12345 डिटेल्स" | Hindi | get_order_details | Detailed information about order #12345 in Hindi |
| "ऑर्डर #12345 को डिलीवर्ड मार्क करो" | Hindi | update_order_status | Confirmation of status update to delivered in Hindi |
| "12345 डिलीवर्ड" | Hindi | update_order_status | Confirmation of status update to delivered in Hindi |

#### Hinglish Examples (Romanized Hindi)

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "Mere recent orders dikhao" | Hinglish | get_orders | List of recent orders with basic details |
| "Baaki orders?" | Hinglish | get_orders | List of pending orders with basic details |
| "Order #12345 ka detail dikhao" | Hinglish | get_order_details | Detailed information about order #12345 |
| "12345 details" | Hinglish | get_order_details | Detailed information about order #12345 |
| "Order #12345 ko delivered mark karo" | Hinglish | update_order_status | Confirmation of status update to delivered |
| "12345 delivered" | Hinglish | update_order_status | Confirmation of status update to delivered |

### Reporting Commands

#### English Examples

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "Show me this month's sales report" | English | get_report | Monthly sales report with key metrics |
| "monthly report" | English | get_report | Monthly sales report with key metrics |
| "Create report from March 1 to March 15" | English | get_custom_report | Custom report for specified date range |
| "report 1-15 mar" | English | get_custom_report | Custom report for specified date range |

#### Hindi Examples (Devanagari)

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "इस महीने की सेल्स रिपोर्ट दिखाओ" | Hindi | get_report | Monthly sales report with key metrics in Hindi |
| "मंथली रिपोर्ट" | Hindi | get_report | Monthly sales report with key metrics in Hindi |
| "1 मार्च से 15 मार्च तक की रिपोर्ट बनाओ" | Hindi | get_custom_report | Custom report for specified date range in Hindi |
| "रिपोर्ट 1-15 मार्च" | Hindi | get_custom_report | Custom report for specified date range in Hindi |

#### Hinglish Examples (Romanized Hindi)

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "Is month ki sales report dikhao" | Hinglish | get_report | Monthly sales report with key metrics |
| "Monthly report" | Hinglish | get_report | Monthly sales report with key metrics |
| "1 March se 15 March tak ki report banao" | Hinglish | get_custom_report | Custom report for specified date range |
| "Report 1-15 March" | Hinglish | get_custom_report | Custom report for specified date range |

### Customer Data Commands

#### English Examples

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "Show customer details for phone 9876543210" | English | get_customer_data | Customer profile information for the phone number |
| "customer 9876543210" | English | get_customer_data | Customer profile information for the phone number |

#### Hindi Examples (Devanagari)

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "फोन 9876543210 के कस्टमर डिटेल्स दिखाओ" | Hindi | get_customer_data | Customer profile information in Hindi |
| "कस्टमर 9876543210" | Hindi | get_customer_data | Customer profile information in Hindi |

#### Hinglish Examples (Romanized Hindi)

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "Phone 9876543210 ke customer details dikhao" | Hinglish | get_customer_data | Customer profile information |
| "Customer 9876543210" | Hinglish | get_customer_data | Customer profile information |

## Edge Case Testing Examples

### Typos and Misspellings

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "Show my inevntory" | English | get_inventory | Should recognize despite typo |
| "मेरा इन्वेंट्री दिखाओ" | Hindi | get_inventory | Should recognize despite typo |
| "Mera inventry dikhao" | Hinglish | get_inventory | Should recognize despite typo |

### Mixed Language

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "Show मेरा inventory" | Mixed | get_inventory | Should detect intent despite mixing |
| "ऑर्डर #12345 details दिखाओ" | Mixed | get_order_details | Should detect intent despite mixing |
| "Report 1 मार्च to 15 मार्च" | Mixed | get_custom_report | Should detect intent despite mixing |

### With Emojis

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "📦 check inventory" | English | get_inventory | Should ignore emoji and detect intent |
| "📦 स्टॉक चेक करो" | Hindi | get_inventory | Should ignore emoji and detect intent |
| "📦 Stock check karo" | Hinglish | get_inventory | Should ignore emoji and detect intent |

### Multiple Intents

| Command Input | Expected Language | Expected Intent | Expected Response Pattern |
|---------------|------------------|----------------|---------------------------|
| "check inventory and pending orders" | English | Multiple/Ambiguous | Should identify primary intent or ask for clarification |
| "इन्वेंटरी चेक करो और बाकी ऑर्डर दिखाओ" | Hindi | Multiple/Ambiguous | Should identify primary intent or ask for clarification |
| "Inventory check karo aur pending orders dikhao" | Hinglish | Multiple/Ambiguous | Should identify primary intent or ask for clarification |

## Testing Workflow Example

### Step-by-Step Process

1. **Select a test case** from the examples above
2. **Enter the command** in the testing interface
3. **Record the actual results**:
   - Detected language
   - Predicted intent
   - Confidence score
   - Response text
4. **Compare with expected outcomes**
5. **Mark as Pass/Fail**
6. **Document any issues** using the following format:

```
Test ID: [Category-Language-VariationNumber]
Command: [Exact command text]
Expected Language: [Language]
Actual Language: [Detected language]
Expected Intent: [Intent]
Actual Intent: [Detected intent]
Confidence Score: [Score]
Expected Response: [Pattern description]
Actual Response: [Exact response text]
Status: [Pass/Fail]
Issue Type: [Mismatch intent/Wrong language detection/Poor confidence/Grammar errors/Missing or awkward replies]
Notes: [Additional observations]
```

## Example Test Execution

### English Inventory Test

```
Test ID: INV-EN-01
Command: "Show my inventory"
Expected Language: English
Actual Language: English
Expected Intent: get_inventory
Actual Intent: get_inventory
Confidence Score: 95%
Expected Response: List of inventory items with quantities
Actual Response: "Here is your current inventory:\n- Product A: 50 units\n- Product B: 25 units\n- Product C: 10 units"
Status: Pass
Issue Type: None
Notes: Response is clear and matches expected format
```

### Hindi Order Test

```
Test ID: ORD-HI-02
Command: "ऑर्डर #12345 का विवरण दिखाओ"
Expected Language: Hindi
Actual Language: Hindi
Expected Intent: get_order_details
Actual Intent: get_order_details
Confidence Score: 88%
Expected Response: Detailed information about order #12345 in Hindi
Actual Response: "ऑर्डर #12345 का विवरण:\nग्राहक: राहुल शर्मा\nराशि: ₹1,500\nस्थिति: प्रोसेसिंग\nआइटम: प्रोडक्ट A (2), प्रोडक्ट B (1)"
Status: Pass
Issue Type: None
Notes: Response is in Hindi and contains all expected order details
```

### Hinglish Report Test with Issue

```
Test ID: REP-HG-01
Command: "Is month ki sales report dikhao"
Expected Language: Hinglish
Actual Language: English
Expected Intent: get_report
Actual Intent: get_custom_report
Confidence Score: 65%
Expected Response: Monthly sales report with key metrics
Actual Response: "Please specify the date range for your custom report."
Status: Fail
Issue Type: Wrong language detection, Mismatch intent, Poor confidence
Notes: System detected language as English instead of Hinglish, misunderstood the intent as custom report instead of monthly report, and had low confidence score.
```

## Response Quality Assessment

For each response, evaluate the following aspects using the 1-5 scale from the language quality assessment rubric:

1. **Grammatical Accuracy:** Is the response grammatically correct?
2. **Vocabulary Appropriateness:** Is the vocabulary suitable for the context?
3. **Cultural Appropriateness:** Does the response respect cultural norms?
4. **Clarity:** Is the response clear and unambiguous?
5. **Consistency:** Is the response consistent with previous responses?
6. **Natural Language Flow:** Does the response sound natural?
7. **Tone:** Is the tone friendly, helpful, and simple?

## Testing Tips

1. **Test in Batches:** Group similar commands together for efficiency
2. **Document Immediately:** Record results right after each test
3. **Look for Patterns:** Note any recurring issues across languages
4. **Test Edge Cases Thoroughly:** These often reveal hidden issues
5. **Compare Across Languages:** Note differences in handling the same intent

## Common Issues to Watch For

1. **Language Detection Issues:**
   - Hindi in Devanagari script detected as another language
   - Hinglish confused with English
   - Mixed language inputs causing detection failures

2. **Intent Recognition Issues:**
   - Casual commands not recognized
   - Regional expressions misunderstood
   - Commands with typos failing completely

3. **Response Quality Issues:**
   - Grammatical errors in Hindi responses
   - Inconsistent terminology across languages
   - Awkward translations
   - Missing information in non-English responses

## Conclusion

This practical testing guide provides concrete examples and expected outcomes for testing the WhatsApp chatbot across English, Hindi, and Hinglish. By following this guide alongside the comprehensive test execution plan, testers can efficiently evaluate the chatbot's multilingual capabilities and document issues in a standardized format.

---

*This document should be used in conjunction with the comprehensive test execution plan and other test planning documents.*