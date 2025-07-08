# Multilingual WhatsApp Chatbot Test Case Matrix

## Overview
This test case matrix provides a comprehensive framework for testing the WhatsApp chatbot across English, Hindi (Devanagari), and Hinglish (Romanized Hindi). It organizes test cases by command category and includes variations for each command type to ensure thorough coverage.

## How to Use This Matrix

1. **Test ID Format:** Each test case has a unique ID in the format `[Category]-[Language]-[Number]`
   - Categories: INV (Inventory), ORD (Order), REP (Report), CUS (Customer), EDG (Edge Case)
   - Languages: ENG (English), HIN (Hindi), HGL (Hinglish)
   - Example: INV-ENG-01 = First inventory test case in English

2. **Testing Process:**
   - Test all variations for each command type
   - Record results using the test results template
   - Note any issues or observations
   - Compare results across languages

3. **Priority Levels:**
   - P1: Critical functionality, must test
   - P2: Important functionality, should test
   - P3: Nice to have, test if time permits

## Test Case Matrix

### 1. Inventory Management Commands

#### 1.1 Get Inventory

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| INV-ENG-01 | English | "Show my inventory" | GetInventory | P1 |
| INV-ENG-02 | English | "What's in my inventory?" | GetInventory | P1 |
| INV-ENG-03 | English | "inventory status" | GetInventory | P1 |
| INV-ENG-04 | English | "check stock" | GetInventory | P2 |
| INV-ENG-05 | English | "show all products in stock" | GetInventory | P2 |
| INV-HIN-01 | Hindi | "मेरा इन्वेंटरी दिखाओ" | GetInventory | P1 |
| INV-HIN-02 | Hindi | "स्टॉक की जानकारी दें" | GetInventory | P1 |
| INV-HIN-03 | Hindi | "इन्वेंटरी स्टेटस" | GetInventory | P1 |
| INV-HIN-04 | Hindi | "सामान का हिसाब दिखाओ" | GetInventory | P2 |
| INV-HIN-05 | Hindi | "मौजूदा स्टॉक क्या है?" | GetInventory | P2 |
| INV-HGL-01 | Hinglish | "Mera inventory dikhao" | GetInventory | P1 |
| INV-HGL-02 | Hinglish | "Stock ki jankari do" | GetInventory | P1 |
| INV-HGL-03 | Hinglish | "Inventory status" | GetInventory | P1 |
| INV-HGL-04 | Hinglish | "Saman ka hisab dikhao" | GetInventory | P2 |
| INV-HGL-05 | Hinglish | "Maujuda stock kya hai?" | GetInventory | P2 |

#### 1.2 Get Low Stock

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| INV-ENG-06 | English | "Show low stock items" | GetLowStock | P1 |
| INV-ENG-07 | English | "which products are running low?" | GetLowStock | P1 |
| INV-ENG-08 | English | "low stock alert" | GetLowStock | P1 |
| INV-ENG-09 | English | "items about to finish" | GetLowStock | P2 |
| INV-ENG-10 | English | "products below minimum quantity" | GetLowStock | P2 |
| INV-HIN-06 | Hindi | "कम स्टॉक वाले आइटम दिखाओ" | GetLowStock | P1 |
| INV-HIN-07 | Hindi | "कौन से प्रोडक्ट कम हो रहे हैं?" | GetLowStock | P1 |
| INV-HIN-08 | Hindi | "लो स्टॉक अलर्ट" | GetLowStock | P1 |
| INV-HIN-09 | Hindi | "खत्म होने वाले सामान" | GetLowStock | P2 |
| INV-HIN-10 | Hindi | "न्यूनतम मात्रा से नीचे प्रोडक्ट" | GetLowStock | P2 |
| INV-HGL-06 | Hinglish | "Kam stock wale item dikhao" | GetLowStock | P1 |
| INV-HGL-07 | Hinglish | "Kaun se product kam ho rahe hain?" | GetLowStock | P1 |
| INV-HGL-08 | Hinglish | "Low stock alert" | GetLowStock | P1 |
| INV-HGL-09 | Hinglish | "Khatam hone wale saman" | GetLowStock | P2 |
| INV-HGL-10 | Hinglish | "Minimum quantity se neeche products" | GetLowStock | P2 |

#### 1.3 Edit Stock

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| INV-ENG-11 | English | "Update stock for product XYZ to 50 units" | EditStock | P1 |
| INV-ENG-12 | English | "change XYZ quantity to 50" | EditStock | P1 |
| INV-ENG-13 | English | "set 50 units for product XYZ" | EditStock | P1 |
| INV-ENG-14 | English | "XYZ stock update 50" | EditStock | P2 |
| INV-ENG-15 | English | "make XYZ stock 50 pieces" | EditStock | P2 |
| INV-HIN-11 | Hindi | "प्रोडक्ट XYZ का स्टॉक 50 यूनिट अपडेट करें" | EditStock | P1 |
| INV-HIN-12 | Hindi | "XYZ की मात्रा 50 करें" | EditStock | P1 |
| INV-HIN-13 | Hindi | "प्रोडक्ट XYZ के लिए 50 यूनिट सेट करें" | EditStock | P1 |
| INV-HIN-14 | Hindi | "XYZ स्टॉक अपडेट 50" | EditStock | P2 |
| INV-HIN-15 | Hindi | "XYZ का स्टॉक 50 पीस करो" | EditStock | P2 |
| INV-HGL-11 | Hinglish | "Product XYZ ka stock 50 unit update karo" | EditStock | P1 |
| INV-HGL-12 | Hinglish | "XYZ ki quantity 50 karo" | EditStock | P1 |
| INV-HGL-13 | Hinglish | "Product XYZ ke liye 50 unit set karo" | EditStock | P1 |
| INV-HGL-14 | Hinglish | "XYZ stock update 50" | EditStock | P2 |
| INV-HGL-15 | Hinglish | "XYZ ka stock 50 piece karo" | EditStock | P2 |

#### 1.4 Add Product

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| INV-ENG-16 | English | "Add new product XYZ with price 100 and quantity 25" | AddProduct | P1 |
| INV-ENG-17 | English | "create product XYZ price 100 qty 25" | AddProduct | P1 |
| INV-ENG-18 | English | "new item XYZ costs 100 stock 25" | AddProduct | P1 |
| INV-ENG-19 | English | "add XYZ to inventory price=100 stock=25" | AddProduct | P2 |
| INV-ENG-20 | English | "create new product called XYZ for 100 rupees with 25 in stock" | AddProduct | P2 |
| INV-HIN-16 | Hindi | "नया प्रोडक्ट XYZ कीमत 100 और मात्रा 25 जोड़ें" | AddProduct | P1 |
| INV-HIN-17 | Hindi | "XYZ प्रोडक्ट बनाएं कीमत 100 मात्रा 25" | AddProduct | P1 |
| INV-HIN-18 | Hindi | "नया आइटम XYZ कीमत 100 स्टॉक 25" | AddProduct | P1 |
| INV-HIN-19 | Hindi | "XYZ को इन्वेंटरी में जोड़ें कीमत=100 स्टॉक=25" | AddProduct | P2 |
| INV-HIN-20 | Hindi | "XYZ नाम का नया प्रोडक्ट 100 रुपये का और 25 स्टॉक के साथ बनाएं" | AddProduct | P2 |
| INV-HGL-16 | Hinglish | "Naya product XYZ price 100 aur quantity 25 add karo" | AddProduct | P1 |
| INV-HGL-17 | Hinglish | "XYZ product banao price 100 quantity 25" | AddProduct | P1 |
| INV-HGL-18 | Hinglish | "Naya item XYZ price 100 stock 25" | AddProduct | P1 |
| INV-HGL-19 | Hinglish | "XYZ ko inventory mein add karo price=100 stock=25" | AddProduct | P2 |
| INV-HGL-20 | Hinglish | "XYZ naam ka naya product 100 rupay ka aur 25 stock ke saath banao" | AddProduct | P2 |

### 2. Order Management Commands

#### 2.1 Get Orders

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| ORD-ENG-01 | English | "Show my recent orders" | GetOrders | P1 |
| ORD-ENG-02 | English | "list all orders" | GetOrders | P1 |
| ORD-ENG-03 | English | "view pending orders" | GetOrders | P1 |
| ORD-ENG-04 | English | "orders from last week" | GetOrders | P2 |
| ORD-ENG-05 | English | "show today's orders" | GetOrders | P2 |
| ORD-HIN-01 | Hindi | "मेरे हाल के ऑर्डर दिखाएं" | GetOrders | P1 |
| ORD-HIN-02 | Hindi | "सभी ऑर्डर की लिस्ट" | GetOrders | P1 |
| ORD-HIN-03 | Hindi | "पेंडिंग ऑर्डर देखें" | GetOrders | P1 |
| ORD-HIN-04 | Hindi | "पिछले हफ्ते के ऑर्डर" | GetOrders | P2 |
| ORD-HIN-05 | Hindi | "आज के ऑर्डर दिखाओ" | GetOrders | P2 |
| ORD-HGL-01 | Hinglish | "Mere recent orders dikhao" | GetOrders | P1 |
| ORD-HGL-02 | Hinglish | "Sabhi orders ki list" | GetOrders | P1 |
| ORD-HGL-03 | Hinglish | "Pending orders dekho" | GetOrders | P1 |
| ORD-HGL-04 | Hinglish | "Pichle hafte ke orders" | GetOrders | P2 |
| ORD-HGL-05 | Hinglish | "Aaj ke orders dikhao" | GetOrders | P2 |

#### 2.2 Get Order Details

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| ORD-ENG-06 | English | "Show details for order #12345" | GetOrderDetails | P1 |
| ORD-ENG-07 | English | "order #12345 info" | GetOrderDetails | P1 |
| ORD-ENG-08 | English | "what's in order 12345" | GetOrderDetails | P1 |
| ORD-ENG-09 | English | "check status of #12345" | GetOrderDetails | P2 |
| ORD-ENG-10 | English | "tell me about order number 12345" | GetOrderDetails | P2 |
| ORD-HIN-06 | Hindi | "ऑर्डर #12345 का विवरण दिखाएं" | GetOrderDetails | P1 |
| ORD-HIN-07 | Hindi | "ऑर्डर #12345 की जानकारी" | GetOrderDetails | P1 |
| ORD-HIN-08 | Hindi | "12345 ऑर्डर में क्या है?" | GetOrderDetails | P1 |
| ORD-HIN-09 | Hindi | "#12345 की स्थिति जांचें" | GetOrderDetails | P2 |
| ORD-HIN-10 | Hindi | "ऑर्डर नंबर 12345 के बारे में बताएं" | GetOrderDetails | P2 |
| ORD-HGL-06 | Hinglish | "Order #12345 ka detail dikhao" | GetOrderDetails | P1 |
| ORD-HGL-07 | Hinglish | "Order #12345 ki info" | GetOrderDetails | P1 |
| ORD-HGL-08 | Hinglish | "12345 order mein kya hai?" | GetOrderDetails | P1 |
| ORD-HGL-09 | Hinglish | "#12345 ka status check karo" | GetOrderDetails | P2 |
| ORD-HGL-10 | Hinglish | "Order number 12345 ke bare mein batao" | GetOrderDetails | P2 |

#### 2.3 Update Order Status

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| ORD-ENG-11 | English | "Mark order #12345 as delivered" | UpdateOrderStatus | P1 |
| ORD-ENG-12 | English | "update #12345 to shipped" | UpdateOrderStatus | P1 |
| ORD-ENG-13 | English | "change order 12345 status to cancelled" | UpdateOrderStatus | P1 |
| ORD-ENG-14 | English | "order 12345 is now delivered" | UpdateOrderStatus | P2 |
| ORD-ENG-15 | English | "set #12345 as completed" | UpdateOrderStatus | P2 |
| ORD-HIN-11 | Hindi | "ऑर्डर #12345 को डिलीवर्ड मार्क करें" | UpdateOrderStatus | P1 |
| ORD-HIN-12 | Hindi | "#12345 को शिप्ड अपडेट करें" | UpdateOrderStatus | P1 |
| ORD-HIN-13 | Hindi | "ऑर्डर 12345 की स्थिति कैंसिल में बदलें" | UpdateOrderStatus | P1 |
| ORD-HIN-14 | Hindi | "ऑर्डर 12345 अब डिलीवर हो गया है" | UpdateOrderStatus | P2 |
| ORD-HIN-15 | Hindi | "#12345 को पूरा हुआ सेट करें" | UpdateOrderStatus | P2 |
| ORD-HGL-11 | Hinglish | "Order #12345 ko delivered mark karo" | UpdateOrderStatus | P1 |
| ORD-HGL-12 | Hinglish | "#12345 ko shipped update karo" | UpdateOrderStatus | P1 |
| ORD-HGL-13 | Hinglish | "Order 12345 ki status cancel mein badlo" | UpdateOrderStatus | P1 |
| ORD-HGL-14 | Hinglish | "Order 12345 ab deliver ho gaya hai" | UpdateOrderStatus | P2 |
| ORD-HGL-15 | Hinglish | "#12345 ko complete set karo" | UpdateOrderStatus | P2 |

### 3. Reporting Commands

#### 3.1 Get Report

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| REP-ENG-01 | English | "Show me this month's sales report" | GetReport | P1 |
| REP-ENG-02 | English | "generate monthly report" | GetReport | P1 |
| REP-ENG-03 | English | "sales summary for April" | GetReport | P1 |
| REP-ENG-04 | English | "how much did we sell this month?" | GetReport | P2 |
| REP-ENG-05 | English | "April business report" | GetReport | P2 |
| REP-HIN-01 | Hindi | "इस महीने की सेल्स रिपोर्ट दिखाएं" | GetReport | P1 |
| REP-HIN-02 | Hindi | "मासिक रिपोर्ट जनरेट करें" | GetReport | P1 |
| REP-HIN-03 | Hindi | "अप्रैल की बिक्री का सारांश" | GetReport | P1 |
| REP-HIN-04 | Hindi | "इस महीने कितना बिका?" | GetReport | P2 |
| REP-HIN-05 | Hindi | "अप्रैल की बिजनेस रिपोर्ट" | GetReport | P2 |
| REP-HGL-01 | Hinglish | "Is month ki sales report dikhao" | GetReport | P1 |
| REP-HGL-02 | Hinglish | "Monthly report generate karo" | GetReport | P1 |
| REP-HGL-03 | Hinglish | "April ki bikri ka summary" | GetReport | P1 |
| REP-HGL-04 | Hinglish | "Is month kitna bika?" | GetReport | P2 |
| REP-HGL-05 | Hinglish | "April ki business report" | GetReport | P2 |

#### 3.2 Get Custom Report

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| REP-ENG-06 | English | "Create report from March 1 to March 15" | GetCustomReport | P1 |
| REP-ENG-07 | English | "custom report last 7 days" | GetCustomReport | P1 |
| REP-ENG-08 | English | "sales data between 01/03 and 15/03" | GetCustomReport | P1 |
| REP-ENG-09 | English | "show me performance from March 1-15" | GetCustomReport | P2 |
| REP-ENG-10 | English | "generate report for first half of March" | GetCustomReport | P2 |
| REP-HIN-06 | Hindi | "1 मार्च से 15 मार्च तक की रिपोर्ट बनाएं" | GetCustomReport | P1 |
| REP-HIN-07 | Hindi | "पिछले 7 दिनों की कस्टम रिपोर्ट" | GetCustomReport | P1 |
| REP-HIN-08 | Hindi | "01/03 और 15/03 के बीच की सेल्स डेटा" | GetCustomReport | P1 |
| REP-HIN-09 | Hindi | "मार्च 1-15 का प्रदर्शन दिखाएं" | GetCustomReport | P2 |
| REP-HIN-10 | Hindi | "मार्च के पहले आधे हिस्से की रिपोर्ट जनरेट करें" | GetCustomReport | P2 |
| REP-HGL-06 | Hinglish | "1 March se 15 March tak ki report banao" | GetCustomReport | P1 |
| REP-HGL-07 | Hinglish | "Last 7 days ki custom report" | GetCustomReport | P1 |
| REP-HGL-08 | Hinglish | "01/03 aur 15/03 ke beech ki sales data" | GetCustomReport | P1 |
| REP-HGL-09 | Hinglish | "March 1-15 ka performance dikhao" | GetCustomReport | P2 |
| REP-HGL-10 | Hinglish | "March ke first half ki report generate karo" | GetCustomReport | P2 |

### 4. Customer Data Commands

#### 4.1 Get Customer Data

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| CUS-ENG-01 | English | "Show customer details for phone 9876543210" | GetCustomerData | P1 |
| CUS-ENG-02 | English | "who is customer 9876543210" | GetCustomerData | P1 |
| CUS-ENG-03 | English | "customer info for 9876543210" | GetCustomerData | P1 |
| CUS-ENG-04 | English | "find customer with number 9876543210" | GetCustomerData | P2 |
| CUS-ENG-05 | English | "get details of buyer 9876543210" | GetCustomerData | P2 |
| CUS-HIN-01 | Hindi | "फोन 9876543210 के लिए ग्राहक विवरण दिखाएं" | GetCustomerData | P1 |
| CUS-HIN-02 | Hindi | "9876543210 कौन ग्राहक है" | GetCustomerData | P1 |
| CUS-HIN-03 | Hindi | "9876543210 के लिए ग्राहक जानकारी" | GetCustomerData | P1 |
| CUS-HIN-04 | Hindi | "9876543210 नंबर वाले ग्राहक को खोजें" | GetCustomerData | P2 |
| CUS-HIN-05 | Hindi | "खरीदार 9876543210 का विवरण प्राप्त करें" | GetCustomerData | P2 |
| CUS-HGL-01 | Hinglish | "Phone 9876543210 ke liye customer details dikhao" | GetCustomerData | P1 |
| CUS-HGL-02 | Hinglish | "9876543210 kaun customer hai" | GetCustomerData | P1 |
| CUS-HGL-03 | Hinglish | "9876543210 ke liye customer info" | GetCustomerData | P1 |
| CUS-HGL-04 | Hinglish | "9876543210 number wale customer ko dhundo" | GetCustomerData | P2 |
| CUS-HGL-05 | Hinglish | "Buyer 9876543210 ka detail nikalo" | GetCustomerData | P2 |

### 5. Edge Cases

#### 5.1 Typos and Misspellings

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| EDG-ENG-01 | English | "Show my inevntory" | GetInventory | P1 |
| EDG-ENG-02 | English | "updaet stock for XYZ to 50" | EditStock | P1 |
| EDG-ENG-03 | English | "get cusotmer details for 9876543210" | GetCustomerData | P1 |
| EDG-HIN-01 | Hindi | "मेरा इनवेंटोरी दिखाओ" | GetInventory | P1 |
| EDG-HIN-02 | Hindi | "प्रोडक्ट XYZ का स्टोक 50 यूनिट अपडेट करें" | EditStock | P1 |
| EDG-HIN-03 | Hindi | "9876543210 के लिए ग्राहक जानकरी" | GetCustomerData | P1 |
| EDG-HGL-01 | Hinglish | "Mera inventri dikhao" | GetInventory | P1 |
| EDG-HGL-02 | Hinglish | "Product XYZ ka stok 50 unit updt kro" | EditStock | P1 |
| EDG-HGL-03 | Hinglish | "9876543210 ke liye custmr info" | GetCustomerData | P1 |

#### 5.2 Abbreviated Text (WhatsApp Style)

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| EDG-HGL-04 | Hinglish | "invntry dkhao" | GetInventory | P1 |
| EDG-HGL-05 | Hinglish | "ordr #12345 ka dtl" | GetOrderDetails | P1 |
| EDG-HGL-06 | Hinglish | "rprt bnao mrch ki" | GetReport | P1 |

#### 5.3 Mixed Language

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| EDG-MIX-01 | Mixed | "Show मेरा inventory" | GetInventory | P1 |
| EDG-MIX-02 | Mixed | "Update प्रोडक्ट XYZ to 50 units" | EditStock | P1 |
| EDG-MIX-03 | Mixed | "Generate अप्रैल की sales report" | GetReport | P1 |
| EDG-MIX-04 | Mixed | "Inventory check kro aur pending orders bhi" | GetInventory | P1 |
| EDG-MIX-05 | Mixed | "XYZ ka price update krke 100 rupees kro" | EditStock | P1 |
| EDG-MIX-06 | Mixed | "Customer ko call krke order #12345 ka status btao" | GetOrderDetails | P1 |
| EDG-MIX-07 | Mixed | "मेरा inventory दिखाओ" | GetInventory | P1 |
| EDG-MIX-08 | Mixed | "प्रोडक्ट XYZ ko 50 यूनिट update करें" | EditStock | P1 |
| EDG-MIX-09 | Mixed | "अप्रैल ki sales report जनरेट करें" | GetReport | P1 |

#### 5.4 Commands with Emojis

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| EDG-EMJ-01 | English | "📦 show inventory" | GetInventory | P2 |
| EDG-EMJ-02 | Hindi | "📦 इन्वेंटरी दिखाओ" | GetInventory | P2 |
| EDG-EMJ-03 | Hinglish | "📦 inventory dikhao" | GetInventory | P2 |
| EDG-EMJ-04 | English | "order #12345 delivered ✅" | UpdateOrderStatus | P2 |
| EDG-EMJ-05 | Hindi | "ऑर्डर #12345 डिलीवर्ड ✅" | UpdateOrderStatus | P2 |
| EDG-EMJ-06 | Hinglish | "order #12345 delivered ✅" | UpdateOrderStatus | P2 |
| EDG-EMJ-07 | English | "sales report 📊 for April" | GetReport | P2 |
| EDG-EMJ-08 | Hindi | "अप्रैल की सेल्स रिपोर्ट 📊" | GetReport | P2 |
| EDG-EMJ-09 | Hinglish | "April ki sales report 📊" | GetReport | P2 |

#### 5.5 Ambiguous Requests

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| EDG-AMB-01 | English | "show everything" | Ambiguous | P2 |
| EDG-AMB-02 | Hindi | "सब कुछ दिखाओ" | Ambiguous | P2 |
| EDG-AMB-03 | Hinglish | "sab kuch dikhao" | Ambiguous | P2 |
| EDG-AMB-04 | English | "update it" | Ambiguous | P2 |
| EDG-AMB-05 | Hindi | "इसे अपडेट करो" | Ambiguous | P2 |
| EDG-AMB-06 | Hinglish | "ise update karo" | Ambiguous | P2 |
| EDG-AMB-07 | English | "check status" | Ambiguous | P2 |
| EDG-AMB-08 | Hindi | "स्थिति जांचें" | Ambiguous | P2 |
| EDG-AMB-09 | Hinglish | "status check karo" | Ambiguous | P2 |

#### 5.6 Multiple Intents

| Test ID | Language | Command Variation | Expected Intent | Priority |
|---------|----------|-------------------|----------------|----------|
| EDG-MLT-01 | English | "show inventory and pending orders" | Multiple | P2 |
| EDG-MLT-02 | Hindi | "इन्वेंटरी और पेंडिंग ऑर्डर दिखाओ" | Multiple | P2 |
| EDG-MLT-03 | Hinglish | "inventory aur pending orders dikhao" | Multiple | P2 |
| EDG-MLT-04 | English | "update stock for XYZ to 50 and create report for April" | Multiple | P2 |
| EDG-MLT-05 | Hindi | "XYZ का स्टॉक 50 अपडेट करें और अप्रैल की रिपोर्ट बनाएं" | Multiple | P2 |
| EDG-MLT-06 | Hinglish | "XYZ ka stock 50 update karo aur April ki report banao" | Multiple | P2 |

## Test Results Recording

For each test case, record the following information:

1. **Test ID:** The unique identifier from this matrix
2. **Command:** The exact text entered
3. **Detected Language:** What language was detected
4. **Predicted Intent:** What intent was recognized
5. **Confidence Score:** The confidence score for the intent
6. **Response:** The chatbot's response
7. **Pass/Fail:** Whether the test passed or failed
8. **Issue Tags:** Any applicable issue tags
9. **Notes:** Additional observations

## Test Execution Strategy

### Recommended Testing Order

1. Start with P1 test cases for each command category in English
2. Move to P1 test cases for Hindi and Hinglish
3. Test edge cases across all languages
4. Complete P2 test cases if time permits

### Efficiency Tips

1. Group similar test cases together to minimize context switching
2. Test the same command across all three languages before moving to the next command
3. Record results immediately after each test
4. Take screenshots of notable issues
5. Look for patterns in failures

## Issue Classification

When a test fails, classify the issue using these tags:

1. **Intent Recognition Issues:**
   - Wrong intent detected
   - No intent detected
   - Low confidence score

2. **Language Detection Issues:**
   - Wrong language detected
   - Mixed language not properly handled

3. **Response Quality Issues:**
   - Grammatical errors
   - Unnatural phrasing
   - Incorrect information
   - Missing information

4. **Edge Case Issues:**
   - Typo handling
   - Abbreviation handling
   - Mixed language handling
   - Emoji handling
   - Multiple intent handling

## Conclusion

This test case matrix provides a comprehensive framework for testing the WhatsApp chatbot across multiple languages. By systematically working through these test cases, testers can identify issues and patterns that will help improve the overall quality of the chatbot's language understanding and response capabilities.

---

*This document should be used alongside the Multilingual WhatsApp Command Testing Plan and related documents.*