# Multilingual WhatsApp Command Testing Plan

## Overview
This document outlines a comprehensive testing plan for evaluating the multilingual capabilities of our WhatsApp command system across three language inputs: English, Hindi (Devanagari), and Hinglish (Romanized Hindi). The focus is on seller-oriented queries related to inventory, billing, and orders.

## Test Objectives
- Verify command recognition across multiple languages
- Evaluate language detection accuracy
- Assess intent prediction confidence
- Test response quality and appropriateness
- Identify edge cases and potential improvements

## Testing Methodology

### Test Environment
- Interface: http://localhost:3000 (Debug NLP UI)
- Test each command with 3-5 variations including:
  - Correct format
  - Minor errors/typos
  - Different phrasing
  - Edge cases

### Data Collection
For each test case, record:
1. Command input (exact text)
2. Detected language
3. Predicted intent
4. Confidence score
5. Output response
6. Pass/Fail status
7. Issue tags (if applicable)

### Issue Classification
Tag issues with one or more of the following:
- **Intent Mismatch**: System detected wrong intent
- **Language Error**: System incorrectly identified the language
- **Low Confidence**: Confidence score below threshold (< 0.7)
- **Response Error**: Grammatical or spelling errors in response
- **Missing Info**: Response lacks critical information
- **Tone Issue**: Response tone inappropriate for context

## Test Cases Matrix

### 1. Inventory Management Commands

| Intent | English | Hindi (Devanagari) | Hinglish (Romanized) |
|--------|---------|---------------------|----------------------|
| Get Inventory | "show my inventory"<br>"list all products"<br>"what's in stock" | "मेरा इन्वेंटरी दिखाओ"<br>"सभी प्रोडक्ट दिखाएं"<br>"स्टॉक में क्या है" | "mera inventory dikhao"<br>"sare products list karo"<br>"stock mein kya hai" |
| Get Low Stock | "show low stock items"<br>"which products are running low"<br>"low inventory alert" | "कम स्टॉक वाले आइटम दिखाएं"<br>"कौन से प्रोडक्ट कम हो रहे हैं"<br>"कम इन्वेंटरी अलर्ट" | "kam stock wale item dikhao"<br>"konse product kam ho rahe hain"<br>"low inventory alert dikhao" |
| Edit Stock | "update stock for product X to 50"<br>"change quantity of X to 20"<br>"set X inventory to 30" | "प्रोडक्ट X का स्टॉक 50 अपडेट करें"<br>"X की मात्रा 20 में बदलें"<br>"X इन्वेंटरी 30 सेट करें" | "product X ka stock 50 update karo"<br>"X ki quantity 20 mein change karo"<br>"X inventory 30 set karo" |
| Add Product | "add new product X price 100 stock 50"<br>"create product X for 100 rs"<br>"new item X at 100" | "नया प्रोडक्ट X कीमत 100 स्टॉक 50 जोड़ें"<br>"प्रोडक्ट X 100 रुपये के लिए बनाएं"<br>"नया आइटम X 100 पर" | "naya product X price 100 stock 50 add karo"<br>"product X 100 rs ke liye banao"<br>"new item X 100 pe" |
| Search Product | "find product X"<br>"search for X"<br>"do I have X in stock" | "प्रोडक्ट X खोजें"<br>"X के लिए खोज"<br>"क्या मेरे पास X स्टॉक में है" | "product X dhundo"<br>"X ke liye search karo"<br>"kya mere pass X stock mein hai" |

### 2. Order Management Commands

| Intent | English | Hindi (Devanagari) | Hinglish (Romanized) |
|--------|---------|---------------------|----------------------|
| Get Orders | "show my orders"<br>"list recent orders"<br>"order history" | "मेरे ऑर्डर दिखाएं"<br>"हाल के ऑर्डर दिखाएं"<br>"ऑर्डर इतिहास" | "mere orders dikhao"<br>"recent orders list karo"<br>"order history" |
| Get Order Details | "show order #12345"<br>"details of order 12345"<br>"what's in order 12345" | "ऑर्डर #12345 दिखाएं"<br>"ऑर्डर 12345 का विवरण"<br>"ऑर्डर 12345 में क्या है" | "order #12345 dikhao"<br>"order 12345 ka details"<br>"order 12345 mein kya hai" |
| Update Order Status | "mark order 12345 as delivered"<br>"update status of order 12345 to shipped"<br>"change order 12345 to cancelled" | "ऑर्डर 12345 को डिलीवर्ड मार्क करें"<br>"ऑर्डर 12345 की स्थिति शिप्ड अपडेट करें"<br>"ऑर्डर 12345 को कैंसल्ड में बदलें" | "order 12345 ko delivered mark karo"<br>"order 12345 ki status shipped update karo"<br>"order 12345 ko cancelled mein badlo" |

### 3. Reporting Commands

| Intent | English | Hindi (Devanagari) | Hinglish (Romanized) |
|--------|---------|---------------------|----------------------|
| Get Report | "show sales report"<br>"get monthly report"<br>"sales summary" | "सेल्स रिपोर्ट दिखाएं"<br>"मासिक रिपोर्ट प्राप्त करें"<br>"बिक्री सारांश" | "sales report dikhao"<br>"monthly report do"<br>"bikri summary" |
| Get Custom Report | "show sales from Jan 1 to Feb 28"<br>"report for last quarter"<br>"weekly sales data" | "1 जनवरी से 28 फरवरी तक की बिक्री दिखाएं"<br>"पिछले तिमाही के लिए रिपोर्ट"<br>"साप्ताहिक बिक्री डेटा" | "1 January se 28 February tak ki bikri dikhao"<br>"last quarter ki report"<br>"weekly sales data" |
| Get Top Products | "show best selling products"<br>"top 5 items this month"<br>"which products sell most" | "सबसे अधिक बिकने वाले प्रोडक्ट दिखाएं"<br>"इस महीने के टॉप 5 आइटम"<br>"कौन से प्रोडक्ट सबसे ज्यादा बिकते हैं" | "best selling products dikhao"<br>"is month ke top 5 item"<br>"konse products sabse jyada bikte hain" |

### 4. Customer Data Commands

| Intent | English | Hindi (Devanagari) | Hinglish (Romanized) |
|--------|---------|---------------------|----------------------|
| Get Customer Data | "show customer details for 9876543210"<br>"customer info for John"<br>"find customer by phone 9876543210" | "9876543210 के लिए ग्राहक विवरण दिखाएं"<br>"जॉन के लिए ग्राहक जानकारी"<br>"फोन 9876543210 द्वारा ग्राहक खोजें" | "9876543210 ke liye customer details dikhao"<br>"John ke liye customer info"<br>"phone 9876543210 se customer dhundo" |

### 5. Edge Cases & Challenging Inputs

| Category | English | Hindi (Devanagari) | Hinglish (Romanized) |
|----------|---------|---------------------|----------------------|
| Mixed Language | "show mera inventory"<br>"update stock of चावल to 50" | "मेरे orders दिखाओ"<br>"product rice का stock update करें" | "meri inventory mein kitna chawal hai"<br>"order #12345 ka status kya hai" |
| Typos & Misspellings | "show my inevntory"<br>"get ordesr"<br>"low sotck" | "मेरा इनवेंटोरी दिखाओ"<br>"ऑर्डर्स दिखाएँ" | "mera invetory dikhao"<br>"ordar history"<br>"stok update karo" |
| Ambiguous Commands | "show everything"<br>"update it"<br>"check status" | "सब दिखाओ"<br>"इसे अपडेट करें"<br>"स्थिति जांचें" | "sab dikhao"<br>"isko update karo"<br>"status check karo" |
| Complex Queries | "show low stock items and update order #12345"<br>"add product X and show sales report" | "कम स्टॉक आइटम दिखाएं और ऑर्डर #12345 अपडेट करें"<br>"प्रोडक्ट X जोड़ें और सेल्स रिपोर्ट दिखाएं" | "kam stock item dikhao aur order #12345 update karo"<br>"product X add karo aur sales report dikhao" |

## Test Results Template

| # | Command Input | Language Detected | Intent Predicted | Confidence | Response | Status | Issues |
|---|--------------|-------------------|-----------------|------------|----------|--------|--------|
| 1 | | | | | | ✔️/❌ | |
| 2 | | | | | | ✔️/❌ | |

## Reporting Guidelines

### Color Coding
- **Green** (Pass): Command correctly processed, appropriate response
- **Yellow** (Warning): Command processed but with issues (low confidence, minor response problems)
- **Red** (Fail): Command misinterpreted or failed to process

### Final Report Format
- Google Sheet shared with team
- Summary tab with overall statistics
- Individual tabs for each intent category
- Screenshots of notable issues
- Recommendations for improvement

## Testing Schedule
- Day 1: Inventory Management Commands
- Day 2: Order Management Commands
- Day 3: Reporting Commands
- Day 4: Customer Data Commands & Edge Cases
- Day 5: Analysis and Report Preparation

## Notes for Testers
- Focus on real-world seller queries and language patterns
- Include common misspellings and slang in Hinglish tests
- Evaluate response clarity, brevity, and helpfulness
- Take screenshots of any unexpected behaviors
- Document any patterns in failures for further analysis