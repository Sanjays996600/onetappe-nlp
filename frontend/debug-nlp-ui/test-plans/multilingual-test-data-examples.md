# Multilingual Test Data Examples for WhatsApp Chatbot

## Overview
This document provides realistic test data examples for WhatsApp chatbot testing in English, Hindi (Devanagari), and Hinglish (Romanized Hindi). These examples cover various command categories and include both standard formats and variations to test the chatbot's language understanding capabilities.

## English Test Data

### Inventory Management

#### Get Inventory
- Standard: "Show me my inventory"
- Variations:
  - "What's in my inventory?"
  - "inventory status"
  - "check stock"
  - "show all products in stock"

#### Get Low Stock
- Standard: "Show low stock items"
- Variations:
  - "which products are running low?"
  - "low stock alert"
  - "items about to finish"
  - "products below minimum quantity"

#### Edit Stock
- Standard: "Update stock for product XYZ to 50 units"
- Variations:
  - "change XYZ quantity to 50"
  - "set 50 units for product XYZ"
  - "XYZ stock update 50"
  - "make XYZ stock 50 pieces"

#### Add Product
- Standard: "Add new product XYZ with price 100 and quantity 25"
- Variations:
  - "create product XYZ price 100 qty 25"
  - "new item XYZ costs 100 stock 25"
  - "add XYZ to inventory price=100 stock=25"
  - "create new product called XYZ for 100 rupees with 25 in stock"

### Order Management

#### Get Orders
- Standard: "Show my recent orders"
- Variations:
  - "list all orders"
  - "view pending orders"
  - "orders from last week"
  - "show today's orders"

#### Get Order Details
- Standard: "Show details for order #12345"
- Variations:
  - "order #12345 info"
  - "what's in order 12345"
  - "check status of #12345"
  - "tell me about order number 12345"

#### Update Order Status
- Standard: "Mark order #12345 as delivered"
- Variations:
  - "update #12345 to shipped"
  - "change order 12345 status to cancelled"
  - "order 12345 is now delivered"
  - "set #12345 as completed"

### Reporting

#### Get Report
- Standard: "Show me this month's sales report"
- Variations:
  - "generate monthly report"
  - "sales summary for April"
  - "how much did we sell this month?"
  - "April business report"

#### Get Custom Report
- Standard: "Create report from March 1 to March 15"
- Variations:
  - "custom report last 7 days"
  - "sales data between 01/03 and 15/03"
  - "show me performance from March 1-15"
  - "generate report for first half of March"

### Customer Data

#### Get Customer Data
- Standard: "Show customer details for phone 9876543210"
- Variations:
  - "who is customer 9876543210"
  - "customer info for 9876543210"
  - "find customer with number 9876543210"
  - "get details of buyer 9876543210"

### Edge Cases

#### Typos and Misspellings
- "Show my inevntory"
- "updaet stock for XYZ to 50"
- "get cusotmer details for 9876543210"

#### Ambiguous Requests
- "show everything"
- "update it"
- "check status"

#### Multiple Intents
- "show inventory and pending orders"
- "update stock for XYZ to 50 and create report for April"

## Hindi (Devanagari) Test Data

### Inventory Management

#### Get Inventory
- Standard: "मेरा इन्वेंटरी दिखाओ"
- Variations:
  - "स्टॉक की जानकारी दें"
  - "इन्वेंटरी स्टेटस"
  - "सामान का हिसाब दिखाओ"
  - "मौजूदा स्टॉक क्या है?"

#### Get Low Stock
- Standard: "कम स्टॉक वाले आइटम दिखाओ"
- Variations:
  - "कौन से प्रोडक्ट कम हो रहे हैं?"
  - "लो स्टॉक अलर्ट"
  - "खत्म होने वाले सामान"
  - "न्यूनतम मात्रा से नीचे प्रोडक्ट"

#### Edit Stock
- Standard: "प्रोडक्ट XYZ का स्टॉक 50 यूनिट अपडेट करें"
- Variations:
  - "XYZ की मात्रा 50 करें"
  - "प्रोडक्ट XYZ के लिए 50 यूनिट सेट करें"
  - "XYZ स्टॉक अपडेट 50"
  - "XYZ का स्टॉक 50 पीस करो"

#### Add Product
- Standard: "नया प्रोडक्ट XYZ कीमत 100 और मात्रा 25 जोड़ें"
- Variations:
  - "XYZ प्रोडक्ट बनाएं कीमत 100 मात्रा 25"
  - "नया आइटम XYZ कीमत 100 स्टॉक 25"
  - "XYZ को इन्वेंटरी में जोड़ें कीमत=100 स्टॉक=25"
  - "XYZ नाम का नया प्रोडक्ट 100 रुपये का और 25 स्टॉक के साथ बनाएं"

### Order Management

#### Get Orders
- Standard: "मेरे हाल के ऑर्डर दिखाएं"
- Variations:
  - "सभी ऑर्डर की लिस्ट"
  - "पेंडिंग ऑर्डर देखें"
  - "पिछले हफ्ते के ऑर्डर"
  - "आज के ऑर्डर दिखाओ"

#### Get Order Details
- Standard: "ऑर्डर #12345 का विवरण दिखाएं"
- Variations:
  - "ऑर्डर #12345 की जानकारी"
  - "12345 ऑर्डर में क्या है?"
  - "#12345 की स्थिति जांचें"
  - "ऑर्डर नंबर 12345 के बारे में बताएं"

#### Update Order Status
- Standard: "ऑर्डर #12345 को डिलीवर्ड मार्क करें"
- Variations:
  - "#12345 को शिप्ड अपडेट करें"
  - "ऑर्डर 12345 की स्थिति कैंसिल में बदलें"
  - "ऑर्डर 12345 अब डिलीवर हो गया है"
  - "#12345 को पूरा हुआ सेट करें"

### Reporting

#### Get Report
- Standard: "इस महीने की सेल्स रिपोर्ट दिखाएं"
- Variations:
  - "मासिक रिपोर्ट जनरेट करें"
  - "अप्रैल की बिक्री का सारांश"
  - "इस महीने कितना बिका?"
  - "अप्रैल की बिजनेस रिपोर्ट"

#### Get Custom Report
- Standard: "1 मार्च से 15 मार्च तक की रिपोर्ट बनाएं"
- Variations:
  - "पिछले 7 दिनों की कस्टम रिपोर्ट"
  - "01/03 और 15/03 के बीच की सेल्स डेटा"
  - "मार्च 1-15 का प्रदर्शन दिखाएं"
  - "मार्च के पहले आधे हिस्से की रिपोर्ट जनरेट करें"

### Customer Data

#### Get Customer Data
- Standard: "फोन 9876543210 के लिए ग्राहक विवरण दिखाएं"
- Variations:
  - "9876543210 कौन ग्राहक है"
  - "9876543210 के लिए ग्राहक जानकारी"
  - "9876543210 नंबर वाले ग्राहक को खोजें"
  - "खरीदार 9876543210 का विवरण प्राप्त करें"

### Edge Cases

#### Typos and Misspellings
- "मेरा इनवेंटोरी दिखाओ"
- "प्रोडक्ट XYZ का स्टोक 50 यूनिट अपडेट करें"
- "9876543210 के लिए ग्राहक जानकरी"

#### Ambiguous Requests
- "सब कुछ दिखाओ"
- "इसे अपडेट करो"
- "स्थिति जांचें"

#### Multiple Intents
- "इन्वेंटरी और पेंडिंग ऑर्डर दिखाओ"
- "XYZ का स्टॉक 50 अपडेट करें और अप्रैल की रिपोर्ट बनाएं"

## Hinglish (Romanized Hindi) Test Data

### Inventory Management

#### Get Inventory
- Standard: "Mera inventory dikhao"
- Variations:
  - "Stock ki jankari do"
  - "Inventory status"
  - "Saman ka hisab dikhao"
  - "Maujuda stock kya hai?"

#### Get Low Stock
- Standard: "Kam stock wale item dikhao"
- Variations:
  - "Kaun se product kam ho rahe hain?"
  - "Low stock alert"
  - "Khatam hone wale saman"
  - "Minimum quantity se neeche products"

#### Edit Stock
- Standard: "Product XYZ ka stock 50 unit update karo"
- Variations:
  - "XYZ ki quantity 50 karo"
  - "Product XYZ ke liye 50 unit set karo"
  - "XYZ stock update 50"
  - "XYZ ka stock 50 piece karo"

#### Add Product
- Standard: "Naya product XYZ price 100 aur quantity 25 add karo"
- Variations:
  - "XYZ product banao price 100 quantity 25"
  - "Naya item XYZ price 100 stock 25"
  - "XYZ ko inventory mein add karo price=100 stock=25"
  - "XYZ naam ka naya product 100 rupay ka aur 25 stock ke saath banao"

### Order Management

#### Get Orders
- Standard: "Mere recent orders dikhao"
- Variations:
  - "Sabhi orders ki list"
  - "Pending orders dekho"
  - "Pichle hafte ke orders"
  - "Aaj ke orders dikhao"

#### Get Order Details
- Standard: "Order #12345 ka detail dikhao"
- Variations:
  - "Order #12345 ki info"
  - "12345 order mein kya hai?"
  - "#12345 ka status check karo"
  - "Order number 12345 ke bare mein batao"

#### Update Order Status
- Standard: "Order #12345 ko delivered mark karo"
- Variations:
  - "#12345 ko shipped update karo"
  - "Order 12345 ki status cancel mein badlo"
  - "Order 12345 ab deliver ho gaya hai"
  - "#12345 ko complete set karo"

### Reporting

#### Get Report
- Standard: "Is month ki sales report dikhao"
- Variations:
  - "Monthly report generate karo"
  - "April ki bikri ka summary"
  - "Is month kitna bika?"
  - "April ki business report"

#### Get Custom Report
- Standard: "1 March se 15 March tak ki report banao"
- Variations:
  - "Last 7 days ki custom report"
  - "01/03 aur 15/03 ke beech ki sales data"
  - "March 1-15 ka performance dikhao"
  - "March ke first half ki report generate karo"

### Customer Data

#### Get Customer Data
- Standard: "Phone 9876543210 ke liye customer details dikhao"
- Variations:
  - "9876543210 kaun customer hai"
  - "9876543210 ke liye customer info"
  - "9876543210 number wale customer ko dhundo"
  - "Buyer 9876543210 ka detail nikalo"

### Edge Cases

#### Typos and Misspellings
- "Mera inventri dikhao"
- "Product XYZ ka stok 50 unit updt kro"
- "9876543210 ke liye custmr info"

#### Abbreviated Text (WhatsApp Style)
- "invntry dkhao"
- "ordr #12345 ka dtl"
- "rprt bnao mrch ki"

#### Mixed Language
- "Inventory check kro aur pending orders bhi"
- "XYZ ka price update krke 100 rupees kro"
- "Customer ko call krke order #12345 ka status btao"

#### With Emojis
- "📦 inventory dikhao"
- "order #12345 delivered ✅ mark karo"
- "sales report 📊 march ki"

## Testing Tips

1. **Test with Real-World Variations**
   - Use natural language variations that real users would type
   - Include common typos and abbreviations
   - Mix formal and informal language styles

2. **Test Language Detection**
   - Try the same command in different languages
   - Use mixed language commands (e.g., English words in Hindi sentences)
   - Test with regional variations of Hindi

3. **Test Intent Recognition**
   - Try different ways of expressing the same intent
   - Use both direct and indirect phrasing
   - Include both complete sentences and abbreviated commands

4. **Test Edge Cases**
   - Commands with multiple intents
   - Very short or ambiguous commands
   - Commands with emojis or special characters
   - Commands with numbers in different formats

5. **Response Evaluation**
   - Check if the response is in the same language as the command
   - Evaluate grammatical correctness and natural flow
   - Assess whether the response addresses the intent correctly
   - Check for consistency in terminology and tone

## Test Data Organization

When using these test examples, organize your testing as follows:

1. Test each command type in all three languages before moving to the next command type
2. For each command type, test the standard format first, then variations
3. Record results consistently using the provided test results template
4. Note any patterns in language detection or intent recognition issues

---

*This document should be used alongside the Multilingual WhatsApp Command Testing Plan and related documents.*