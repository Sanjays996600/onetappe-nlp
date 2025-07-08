# हिंदी-अंग्रेजी विस्तृत परीक्षण मामले
# Hindi-English Detailed Test Cases

## परिचय / Introduction

इस दस्तावेज़ में One Tappe व्हाट्सएप चैटबॉट के हिंदी और अंग्रेजी भाषा समर्थन के लिए विस्तृत परीक्षण मामले शामिल हैं। ये परीक्षण मामले विभिन्न इंटेंट, एंटिटी और प्रतिक्रिया प्रकारों को कवर करते हैं और यह सुनिश्चित करते हैं कि चैटबॉट दोनों भाषाओं में प्रभावी ढंग से संवाद कर सके।

This document contains detailed test cases for Hindi and English language support in the One Tappe WhatsApp chatbot. These test cases cover various intents, entities, and response types and ensure that the chatbot can communicate effectively in both languages.

## परीक्षण मामले वर्गीकरण / Test Case Classification

परीक्षण मामलों को निम्नलिखित श्रेणियों में वर्गीकृत किया गया है:

Test cases are classified into the following categories:

1. **इंटेंट पहचान परीक्षण / Intent Recognition Tests (IR)**
2. **एंटिटी निष्कर्षण परीक्षण / Entity Extraction Tests (EE)**
3. **प्रतिक्रिया गुणवत्ता परीक्षण / Response Quality Tests (RQ)**
4. **भाषा स्विचिंग परीक्षण / Language Switching Tests (LS)**
5. **त्रुटि प्रबंधन परीक्षण / Error Handling Tests (EH)**

## 1. इंटेंट पहचान परीक्षण / Intent Recognition Tests (IR)

### IR-001: अंग्रेजी में इन्वेंटरी कमांड / Inventory Commands in English

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट अंग्रेजी में इन्वेंटरी कमांड को सही ढंग से पहचानता है / Verify that the chatbot correctly recognizes inventory commands in English

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित इंटेंट / Expected Intent |
|---------------------|---------------------------|--------------------------------|
| 1 | Show me my inventory | `get_inventory` |
| 2 | What's in my stock? | `get_inventory` |
| 3 | List all products | `get_inventory` |
| 4 | Show inventory | `get_inventory` |
| 5 | Current stock | `get_inventory` |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट प्रत्येक इनपुट को `get_inventory` इंटेंट के रूप में पहचानता है / Chatbot recognizes each input as `get_inventory` intent
- चैटबॉट इन्वेंटरी की सूची के साथ प्रतिक्रिया देता है / Chatbot responds with a list of inventory

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

### IR-002: हिंदी में इन्वेंटरी कमांड / Inventory Commands in Hindi

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट हिंदी में इन्वेंटरी कमांड को सही ढंग से पहचानता है / Verify that the chatbot correctly recognizes inventory commands in Hindi

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित इंटेंट / Expected Intent |
|---------------------|---------------------------|--------------------------------|
| 1 | मेरा इन्वेंटरी दिखाओ | `get_inventory` |
| 2 | स्टॉक में क्या है? | `get_inventory` |
| 3 | सभी प्रोडक्ट दिखाओ | `get_inventory` |
| 4 | इन्वेंटरी दिखाओ | `get_inventory` |
| 5 | वर्तमान स्टॉक | `get_inventory` |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट प्रत्येक इनपुट को `get_inventory` इंटेंट के रूप में पहचानता है / Chatbot recognizes each input as `get_inventory` intent
- चैटबॉट हिंदी में इन्वेंटरी की सूची के साथ प्रतिक्रिया देता है / Chatbot responds with a list of inventory in Hindi

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

### IR-003: अंग्रेजी में स्टॉक अपडेट कमांड / Stock Update Commands in English

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट अंग्रेजी में स्टॉक अपडेट कमांड को सही ढंग से पहचानता है / Verify that the chatbot correctly recognizes stock update commands in English

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp
- इन्वेंटरी में कम से कम एक प्रोडक्ट है / There is at least one product in the inventory

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित इंटेंट / Expected Intent |
|---------------------|---------------------------|--------------------------------|
| 1 | Update rice stock to 100 | `edit_stock` |
| 2 | Change sugar quantity to 50 | `edit_stock` |
| 3 | Set wheat stock to 200 | `edit_stock` |
| 4 | Make oil stock 30 | `edit_stock` |
| 5 | Update dal to 150 pieces | `edit_stock` |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट प्रत्येक इनपुट को `edit_stock` इंटेंट के रूप में पहचानता है / Chatbot recognizes each input as `edit_stock` intent
- चैटबॉट स्टॉक अपडेट की पुष्टि के साथ प्रतिक्रिया देता है / Chatbot responds with confirmation of stock update

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

### IR-004: हिंदी में स्टॉक अपडेट कमांड / Stock Update Commands in Hindi

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट हिंदी में स्टॉक अपडेट कमांड को सही ढंग से पहचानता है / Verify that the chatbot correctly recognizes stock update commands in Hindi

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp
- इन्वेंटरी में कम से कम एक प्रोडक्ट है / There is at least one product in the inventory

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित इंटेंट / Expected Intent |
|---------------------|---------------------------|--------------------------------|
| 1 | चावल का स्टॉक 100 करो | `edit_stock` |
| 2 | चीनी की मात्रा 50 करो | `edit_stock` |
| 3 | गेहूं का स्टॉक 200 सेट करो | `edit_stock` |
| 4 | तेल का स्टॉक 30 करो | `edit_stock` |
| 5 | दाल को 150 पीस अपडेट करो | `edit_stock` |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट प्रत्येक इनपुट को `edit_stock` इंटेंट के रूप में पहचानता है / Chatbot recognizes each input as `edit_stock` intent
- चैटबॉट हिंदी में स्टॉक अपडेट की पुष्टि के साथ प्रतिक्रिया देता है / Chatbot responds with confirmation of stock update in Hindi

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

### IR-005: अंग्रेजी में रिपोर्ट कमांड / Report Commands in English

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट अंग्रेजी में रिपोर्ट कमांड को सही ढंग से पहचानता है / Verify that the chatbot correctly recognizes report commands in English

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित इंटेंट / Expected Intent |
|---------------------|---------------------------|--------------------------------|
| 1 | Show me the report from 1st June to 30th June | `get_report` |
| 2 | Get sales report for last month | `get_report` |
| 3 | Show report for January | `get_report` |
| 4 | I need a report for this week | `get_report` |
| 5 | Generate report from 10/05/2023 to 20/05/2023 | `get_report` |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट प्रत्येक इनपुट को `get_report` इंटेंट के रूप में पहचानता है / Chatbot recognizes each input as `get_report` intent
- चैटबॉट निर्दिष्ट समय अवधि के लिए रिपोर्ट के साथ प्रतिक्रिया देता है / Chatbot responds with a report for the specified time period

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

### IR-006: हिंदी में रिपोर्ट कमांड / Report Commands in Hindi

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट हिंदी में रिपोर्ट कमांड को सही ढंग से पहचानता है / Verify that the chatbot correctly recognizes report commands in Hindi

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित इंटेंट / Expected Intent |
|---------------------|---------------------------|--------------------------------|
| 1 | 1 जून से 30 जून तक की रिपोर्ट दिखाओ | `get_report` |
| 2 | पिछले महीने की बिक्री रिपोर्ट दिखाओ | `get_report` |
| 3 | जनवरी की रिपोर्ट दिखाओ | `get_report` |
| 4 | इस हफ्ते की रिपोर्ट चाहिए | `get_report` |
| 5 | 10/05/2023 से 20/05/2023 तक की रिपोर्ट बनाओ | `get_report` |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट प्रत्येक इनपुट को `get_report` इंटेंट के रूप में पहचानता है / Chatbot recognizes each input as `get_report` intent
- चैटबॉट हिंदी में निर्दिष्ट समय अवधि के लिए रिपोर्ट के साथ प्रतिक्रिया देता है / Chatbot responds with a report for the specified time period in Hindi

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

## 2. एंटिटी निष्कर्षण परीक्षण / Entity Extraction Tests (EE)

### EE-001: अंग्रेजी में प्रोडक्ट नाम और मात्रा / Product Name and Quantity in English

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट अंग्रेजी कमांड से प्रोडक्ट नाम और मात्रा को सही ढंग से निकालता है / Verify that the chatbot correctly extracts product name and quantity from English commands

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित प्रोडक्ट नाम / Expected Product Name | अपेक्षित मात्रा / Expected Quantity |
|---------------------|---------------------------|------------------------------------------|-----------------------------------|
| 1 | Add new product rice 50 rupees 20 pieces | rice | 20 |
| 2 | Update sugar stock to 100 kg | sugar | 100 |
| 3 | Set wheat quantity to 200 | wheat | 200 |
| 4 | Make oil stock 30 liters | oil | 30 |
| 5 | Add new product dal 100 rupees 50 packets | dal | 50 |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट प्रत्येक इनपुट से प्रोडक्ट नाम और मात्रा को सही ढंग से निकालता है / Chatbot correctly extracts product name and quantity from each input
- चैटबॉट निकाली गई जानकारी के आधार पर उचित प्रतिक्रिया देता है / Chatbot gives appropriate response based on the extracted information

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

### EE-002: हिंदी में प्रोडक्ट नाम और मात्रा / Product Name and Quantity in Hindi

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट हिंदी कमांड से प्रोडक्ट नाम और मात्रा को सही ढंग से निकालता है / Verify that the chatbot correctly extracts product name and quantity from Hindi commands

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित प्रोडक्ट नाम / Expected Product Name | अपेक्षित मात्रा / Expected Quantity |
|---------------------|---------------------------|------------------------------------------|-----------------------------------|
| 1 | नया प्रोडक्ट चावल 50 रुपये 20 पीस जोड़ो | चावल | 20 |
| 2 | चीनी का स्टॉक 100 किलो अपडेट करो | चीनी | 100 |
| 3 | गेहूं की मात्रा 200 सेट करो | गेहूं | 200 |
| 4 | तेल का स्टॉक 30 लीटर करो | तेल | 30 |
| 5 | नया प्रोडक्ट दाल 100 रुपये 50 पैकेट जोड़ो | दाल | 50 |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट प्रत्येक इनपुट से प्रोडक्ट नाम और मात्रा को सही ढंग से निकालता है / Chatbot correctly extracts product name and quantity from each input
- चैटबॉट हिंदी में निकाली गई जानकारी के आधार पर उचित प्रतिक्रिया देता है / Chatbot gives appropriate response in Hindi based on the extracted information

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

### EE-003: अंग्रेजी में तिथि सीमा / Date Range in English

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट अंग्रेजी कमांड से तिथि सीमा को सही ढंग से निकालता है / Verify that the chatbot correctly extracts date range from English commands

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित शुरू तिथि / Expected Start Date | अपेक्षित अंत तिथि / Expected End Date |
|---------------------|---------------------------|--------------------------------------|----------------------------------|
| 1 | Show me the report from 1st June to 30th June | 2023-06-01 | 2023-06-30 |
| 2 | Get sales report for last month | [पिछले महीने की पहली तारीख / First day of last month] | [पिछले महीने की अंतिम तारीख / Last day of last month] |
| 3 | Show report for January | 2023-01-01 | 2023-01-31 |
| 4 | I need a report for this week | [इस हफ्ते की पहली तारीख / First day of this week] | [इस हफ्ते की अंतिम तारीख / Last day of this week] |
| 5 | Generate report from 10/05/2023 to 20/05/2023 | 2023-05-10 | 2023-05-20 |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट प्रत्येक इनपुट से तिथि सीमा को सही ढंग से निकालता है / Chatbot correctly extracts date range from each input
- चैटबॉट निकाली गई तिथि सीमा के लिए रिपोर्ट के साथ प्रतिक्रिया देता है / Chatbot responds with a report for the extracted date range

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

### EE-004: हिंदी में तिथि सीमा / Date Range in Hindi

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट हिंदी कमांड से तिथि सीमा को सही ढंग से निकालता है / Verify that the chatbot correctly extracts date range from Hindi commands

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित शुरू तिथि / Expected Start Date | अपेक्षित अंत तिथि / Expected End Date |
|---------------------|---------------------------|--------------------------------------|----------------------------------|
| 1 | 1 जून से 30 जून तक की रिपोर्ट दिखाओ | 2023-06-01 | 2023-06-30 |
| 2 | पिछले महीने की बिक्री रिपोर्ट दिखाओ | [पिछले महीने की पहली तारीख / First day of last month] | [पिछले महीने की अंतिम तारीख / Last day of last month] |
| 3 | जनवरी की रिपोर्ट दिखाओ | 2023-01-01 | 2023-01-31 |
| 4 | इस हफ्ते की रिपोर्ट चाहिए | [इस हफ्ते की पहली तारीख / First day of this week] | [इस हफ्ते की अंतिम तारीख / Last day of this week] |
| 5 | 10/05/2023 से 20/05/2023 तक की रिपोर्ट बनाओ | 2023-05-10 | 2023-05-20 |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट प्रत्येक इनपुट से तिथि सीमा को सही ढंग से निकालता है / Chatbot correctly extracts date range from each input
- चैटबॉट हिंदी में निकाली गई तिथि सीमा के लिए रिपोर्ट के साथ प्रतिक्रिया देता है / Chatbot responds with a report for the extracted date range in Hindi

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

## 3. प्रतिक्रिया गुणवत्ता परीक्षण / Response Quality Tests (RQ)

### RQ-001: अंग्रेजी प्रतिक्रियाओं की व्याकरणिक सटीकता / Grammatical Accuracy of English Responses

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट की अंग्रेजी प्रतिक्रियाएँ व्याकरणिक रूप से सही हैं / Verify that the chatbot's English responses are grammatically correct

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | प्रतिक्रिया का प्रकार / Response Type |
|---------------------|---------------------------|----------------------------------|
| 1 | Show me my inventory | इन्वेंटरी सूची / Inventory list |
| 2 | Update rice stock to 100 | पुष्टिकरण संदेश / Confirmation message |
| 3 | Show me the report from 1st June to 30th June | रिपोर्ट / Report |
| 4 | Add new product rice 50 rupees 20 pieces | पुष्टिकरण संदेश / Confirmation message |
| 5 | What are my top selling products? | उत्पाद सूची / Product list |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response
4. प्रतिक्रिया की व्याकरणिक सटीकता का मूल्यांकन करें / Evaluate the grammatical accuracy of the response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट की प्रतिक्रियाएँ व्याकरणिक रूप से सही होनी चाहिए / Chatbot's responses should be grammatically correct
- प्रतिक्रियाओं में कोई व्याकरण त्रुटि नहीं होनी चाहिए / Responses should not have any grammatical errors

**मूल्यांकन मानदंड / Evaluation Criteria:**
- वाक्य संरचना / Sentence structure
- काल (टेन्स) का उपयोग / Tense usage
- विराम चिह्न / Punctuation
- शब्द क्रम / Word order
- सहमति (सब्जेक्ट-वर्ब एग्रीमेंट) / Subject-verb agreement

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

### RQ-002: हिंदी प्रतिक्रियाओं की व्याकरणिक सटीकता / Grammatical Accuracy of Hindi Responses

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट की हिंदी प्रतिक्रियाएँ व्याकरणिक रूप से सही हैं / Verify that the chatbot's Hindi responses are grammatically correct

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | प्रतिक्रिया का प्रकार / Response Type |
|---------------------|---------------------------|----------------------------------|
| 1 | मेरा इन्वेंटरी दिखाओ | इन्वेंटरी सूची / Inventory list |
| 2 | चावल का स्टॉक 100 करो | पुष्टिकरण संदेश / Confirmation message |
| 3 | 1 जून से 30 जून तक की रिपोर्ट दिखाओ | रिपोर्ट / Report |
| 4 | नया प्रोडक्ट चावल 50 रुपये 20 पीस जोड़ो | पुष्टिकरण संदेश / Confirmation message |
| 5 | मेरे टॉप सेलिंग प्रोडक्ट कौन से हैं? | उत्पाद सूची / Product list |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response
4. प्रतिक्रिया की व्याकरणिक सटीकता का मूल्यांकन करें / Evaluate the grammatical accuracy of the response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट की प्रतिक्रियाएँ व्याकरणिक रूप से सही होनी चाहिए / Chatbot's responses should be grammatically correct
- प्रतिक्रियाओं में कोई व्याकरण त्रुटि नहीं होनी चाहिए / Responses should not have any grammatical errors

**मूल्यांकन मानदंड / Evaluation Criteria:**
- वाक्य संरचना / Sentence structure
- लिंग (जेंडर) का उपयोग / Gender usage
- वचन (नंबर) का उपयोग / Number usage
- परसर्ग (पोस्टपोजिशन) का उपयोग / Postposition usage
- काल (टेन्स) का उपयोग / Tense usage
- विराम चिह्न / Punctuation

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

## 4. भाषा स्विचिंग परीक्षण / Language Switching Tests (LS)

### LS-001: अंग्रेजी से हिंदी में स्विच / Switch from English to Hindi

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट अंग्रेजी से हिंदी में सहज रूप से स्विच कर सकता है / Verify that the chatbot can seamlessly switch from English to Hindi

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित प्रतिक्रिया भाषा / Expected Response Language |
|---------------------|---------------------------|------------------------------------------------|
| 1 | Show me my inventory | अंग्रेजी / English |
| 2 | मेरा स्टॉक दिखाओ | हिंदी / Hindi |
| 3 | Update rice stock to 100 | अंग्रेजी / English |
| 4 | चावल का स्टॉक कितना है? | हिंदी / Hindi |
| 5 | अब हिंदी में बात करो | हिंदी / Hindi |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को क्रम से भेजें / Send each input given in the test data in sequence
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response
4. प्रतिक्रिया की भाषा का मूल्यांकन करें / Evaluate the language of the response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट उपयोगकर्ता के इनपुट की भाषा के अनुसार प्रतिक्रिया देता है / Chatbot responds according to the language of the user's input
- भाषा स्विच के बाद, चैटबॉट नई भाषा में प्रतिक्रिया देना जारी रखता है / After language switch, chatbot continues to respond in the new language

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

### LS-002: हिंदी से अंग्रेजी में स्विच / Switch from Hindi to English

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट हिंदी से अंग्रेजी में सहज रूप से स्विच कर सकता है / Verify that the chatbot can seamlessly switch from Hindi to English

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित प्रतिक्रिया भाषा / Expected Response Language |
|---------------------|---------------------------|------------------------------------------------|
| 1 | मेरा इन्वेंटरी दिखाओ | हिंदी / Hindi |
| 2 | Show me my stock | अंग्रेजी / English |
| 3 | चावल का स्टॉक 100 करो | हिंदी / Hindi |
| 4 | How much rice do I have? | अंग्रेजी / English |
| 5 | Now speak in English | अंग्रेजी / English |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को क्रम से भेजें / Send each input given in the test data in sequence
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response
4. प्रतिक्रिया की भाषा का मूल्यांकन करें / Evaluate the language of the response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट उपयोगकर्ता के इनपुट की भाषा के अनुसार प्रतिक्रिया देता है / Chatbot responds according to the language of the user's input
- भाषा स्विच के बाद, चैटबॉट नई भाषा में प्रतिक्रिया देना जारी रखता है / After language switch, chatbot continues to respond in the new language

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

## 5. त्रुटि प्रबंधन परीक्षण / Error Handling Tests (EH)

### EH-001: अंग्रेजी में अपूर्ण कमांड / Incomplete Commands in English

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट अंग्रेजी में अपूर्ण कमांड को सही ढंग से संभालता है / Verify that the chatbot correctly handles incomplete commands in English

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित प्रतिक्रिया प्रकार / Expected Response Type |
|---------------------|---------------------------|------------------------------------------------|
| 1 | Update stock | अतिरिक्त जानकारी के लिए अनुरोध / Request for additional information |
| 2 | Add new product | अतिरिक्त जानकारी के लिए अनुरोध / Request for additional information |
| 3 | Show report | अतिरिक्त जानकारी के लिए अनुरोध / Request for additional information |
| 4 | Change price | अतिरिक्त जानकारी के लिए अनुरोध / Request for additional information |
| 5 | Search | अतिरिक्त जानकारी के लिए अनुरोध / Request for additional information |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट अपूर्ण कमांड को पहचानता है / Chatbot recognizes the incomplete command
- चैटबॉट अतिरिक्त जानकारी के लिए स्पष्ट अनुरोध के साथ प्रतिक्रिया देता है / Chatbot responds with a clear request for additional information
- प्रतिक्रिया उपयोगकर्ता को आवश्यक जानकारी प्रदान करने के लिए मार्गदर्शन करती है / Response guides the user to provide the necessary information

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

### EH-002: हिंदी में अपूर्ण कमांड / Incomplete Commands in Hindi

**उद्देश्य / Objective:** सत्यापित करें कि चैटबॉट हिंदी में अपूर्ण कमांड को सही ढंग से संभालता है / Verify that the chatbot correctly handles incomplete commands in Hindi

**पूर्व-शर्तें / Preconditions:**
- चैटबॉट सक्रिय है / Chatbot is active
- उपयोगकर्ता ने व्हाट्सएप पर चैटबॉट से संपर्क किया है / User has contacted the chatbot on WhatsApp

**परीक्षण डेटा / Test Data:**

| क्रम संख्या / S.No. | परीक्षण इनपुट / Test Input | अपेक्षित प्रतिक्रिया प्रकार / Expected Response Type |
|---------------------|---------------------------|------------------------------------------------|
| 1 | स्टॉक अपडेट करो | अतिरिक्त जानकारी के लिए अनुरोध / Request for additional information |
| 2 | नया प्रोडक्ट जोड़ो | अतिरिक्त जानकारी के लिए अनुरोध / Request for additional information |
| 3 | रिपोर्ट दिखाओ | अतिरिक्त जानकारी के लिए अनुरोध / Request for additional information |
| 4 | कीमत बदलो | अतिरिक्त जानकारी के लिए अनुरोध / Request for additional information |
| 5 | खोजो | अतिरिक्त जानकारी के लिए अनुरोध / Request for additional information |

**परीक्षण चरण / Test Steps:**
1. व्हाट्सएप पर चैटबॉट से संपर्क करें / Contact the chatbot on WhatsApp
2. परीक्षण डेटा में दिए गए प्रत्येक इनपुट को भेजें / Send each input given in the test data
3. चैटबॉट की प्रतिक्रिया की जांच करें / Check the chatbot's response

**अपेक्षित परिणाम / Expected Results:**
- चैटबॉट अपूर्ण कमांड को पहचानता है / Chatbot recognizes the incomplete command
- चैटबॉट हिंदी में अतिरिक्त जानकारी के लिए स्पष्ट अनुरोध के साथ प्रतिक्रिया देता है / Chatbot responds with a clear request for additional information in Hindi
- प्रतिक्रिया उपयोगकर्ता को आवश्यक जानकारी प्रदान करने के लिए मार्गदर्शन करती है / Response guides the user to provide the necessary information

**वास्तविक परिणाम / Actual Results:**
- [परीक्षण के बाद भरें / To be filled after testing]

**स्थिति / Status:**
- [पास/फेल / Pass/Fail]

**टिप्पणियां / Comments:**
- [कोई अतिरिक्त टिप्पणियां / Any additional comments]

---

## परीक्षण परिणाम सारांश / Test Result Summary

### इंटेंट पहचान परीक्षण / Intent Recognition Tests

| परीक्षण आईडी / Test ID | परीक्षण नाम / Test Name | स्थिति / Status |
|----------------------|------------------------|----------------|
| IR-001 | अंग्रेजी में इन्वेंटरी कमांड / Inventory Commands in English | [पास/फेल / Pass/Fail] |
| IR-002 | हिंदी में इन्वेंटरी कमांड / Inventory Commands in Hindi | [पास/फेल / Pass/Fail] |
| IR-003 | अंग्रेजी में स्टॉक अपडेट कमांड / Stock Update Commands in English | [पास/फेल / Pass/Fail] |
| IR-004 | हिंदी में स्टॉक अपडेट कमांड / Stock Update Commands in Hindi | [पास/फेल / Pass/Fail]