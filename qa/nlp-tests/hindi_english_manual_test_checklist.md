# हिंदी-अंग्रेजी भाषा मैनुअल परीक्षण चेकलिस्ट
# Hindi-English Language Manual Testing Checklist

## परिचय / Introduction

इस दस्तावेज़ में व्हाट्सएप चैटबॉट के हिंदी और अंग्रेजी भाषा समर्थन के मैनुअल परीक्षण के लिए चेकलिस्ट और टेस्ट केस शामिल हैं। यह परीक्षण स्वचालित परीक्षण के पूरक के रूप में है और उन पहलुओं पर ध्यान केंद्रित करता है जिन्हें स्वचालित परीक्षण में कवर नहीं किया जा सकता।

This document contains checklists and test cases for manual testing of Hindi and English language support in the WhatsApp chatbot. This testing complements automated testing and focuses on aspects that cannot be covered in automated tests.

## परीक्षण पूर्व तैयारी / Pre-Testing Preparation

- [ ] परीक्षण के लिए व्हाट्सएप अकाउंट तैयार है / WhatsApp account is ready for testing
- [ ] परीक्षण डेटा (प्रोडक्ट, ऑर्डर, इन्वेंटरी) तैयार है / Test data (products, orders, inventory) is prepared
- [ ] परीक्षण परिणामों को रिकॉर्ड करने के लिए टेम्पलेट तैयार है / Template for recording test results is prepared
- [ ] परीक्षण वातावरण (डेवलपमेंट/स्टेजिंग) तैयार है / Testing environment (development/staging) is ready

## भाषा पहचान परीक्षण / Language Detection Testing

### अंग्रेजी कमांड / English Commands

| ID | परीक्षण मामला / Test Case | अपेक्षित परिणाम / Expected Result | वास्तविक परिणाम / Actual Result | स्थिति / Status |
|----|---------------------------|--------------------------------|------------------------------|---------------|
| LD-EN-001 | Send "Hello" | Language detected as English | | |
| LD-EN-002 | Send "Show my inventory" | Language detected as English | | |
| LD-EN-003 | Send "What's the stock of rice?" | Language detected as English | | |
| LD-EN-004 | Send "I want to see my orders" | Language detected as English | | |
| LD-EN-005 | Send "Can you show me the report for this month?" | Language detected as English | | |

### हिंदी कमांड / Hindi Commands

| ID | परीक्षण मामला / Test Case | अपेक्षित परिणाम / Expected Result | वास्तविक परिणाम / Actual Result | स्थिति / Status |
|----|---------------------------|--------------------------------|------------------------------|---------------|
| LD-HI-001 | Send "नमस्ते" | Language detected as Hindi | | |
| LD-HI-002 | Send "मेरा इन्वेंटरी दिखाओ" | Language detected as Hindi | | |
| LD-HI-003 | Send "चावल का स्टॉक कितना है?" | Language detected as Hindi | | |
| LD-HI-004 | Send "मुझे अपने ऑर्डर देखने हैं" | Language detected as Hindi | | |
| LD-HI-005 | Send "क्या आप मुझे इस महीने की रिपोर्ट दिखा सकते हैं?" | Language detected as Hindi | | |

### मिश्रित भाषा कमांड / Mixed Language Commands

| ID | परीक्षण मामला / Test Case | अपेक्षित परिणाम / Expected Result | वास्तविक परिणाम / Actual Result | स्थिति / Status |
|----|---------------------------|--------------------------------|------------------------------|---------------|
| LD-MX-001 | Send "Hello मेरा नाम राज है" | Language detected correctly | | |
| LD-MX-002 | Send "Show मेरा inventory" | Language detected correctly | | |
| LD-MX-003 | Send "Rice का stock कितना है?" | Language detected correctly | | |
| LD-MX-004 | Send "मुझे orders देखने हैं" | Language detected correctly | | |
| LD-MX-005 | Send "Report दिखाओ for this month" | Language detected correctly | | |

## इंटेंट पहचान परीक्षण / Intent Recognition Testing

### अंग्रेजी वैकल्पिक वाक्यांश / English Alternative Phrases

| ID | परीक्षण मामला / Test Case | अपेक्षित इंटेंट / Expected Intent | वास्तविक इंटेंट / Actual Intent | स्थिति / Status |
|----|---------------------------|--------------------------------|------------------------------|---------------|
| IR-EN-001 | Send "What do I have in stock?" | get_inventory | | |
| IR-EN-002 | Send "How much rice do I have?" | search_product | | |
| IR-EN-003 | Send "I need to update sugar quantity to 25" | edit_stock | | |
| IR-EN-004 | Send "What items are running low?" | get_low_stock | | |
| IR-EN-005 | Send "How did my business do today?" | get_report | | |
| IR-EN-006 | Send "What orders came in yesterday?" | get_orders | | |
| IR-EN-007 | Send "I want to add a new item called wheat flour" | add_product | | |
| IR-EN-008 | Send "Who are my best customers?" | get_customer_data | | |
| IR-EN-009 | Send "What products are selling the most?" | get_top_products | | |
| IR-EN-010 | Send "I need to see my sales performance" | get_report | | |

### हिंदी वैकल्पिक वाक्यांश / Hindi Alternative Phrases

| ID | परीक्षण मामला / Test Case | अपेक्षित इंटेंट / Expected Intent | वास्तविक इंटेंट / Actual Intent | स्थिति / Status |
|----|---------------------------|--------------------------------|------------------------------|---------------|
| IR-HI-001 | Send "मेरे पास क्या स्टॉक है?" | get_inventory | | |
| IR-HI-002 | Send "मेरे पास कितना चावल है?" | search_product | | |
| IR-HI-003 | Send "मुझे चीनी की मात्रा 25 करनी है" | edit_stock | | |
| IR-HI-004 | Send "कौन से आइटम कम हो रहे हैं?" | get_low_stock | | |
| IR-HI-005 | Send "आज मेरा बिजनेस कैसा रहा?" | get_report | | |
| IR-HI-006 | Send "कल कौन से ऑर्डर आए?" | get_orders | | |
| IR-HI-007 | Send "मुझे गेहूं का आटा नाम से एक नया आइटम जोड़ना है" | add_product | | |
| IR-HI-008 | Send "मेरे सबसे अच्छे ग्राहक कौन हैं?" | get_customer_data | | |
| IR-HI-009 | Send "कौन से प्रोडक्ट सबसे ज्यादा बिक रहे हैं?" | get_top_products | | |
| IR-HI-010 | Send "मुझे अपनी बिक्री का प्रदर्शन देखना है" | get_report | | |

## एंटिटी निष्कर्षण परीक्षण / Entity Extraction Testing

### अंग्रेजी एंटिटी निष्कर्षण / English Entity Extraction

| ID | परीक्षण मामला / Test Case | अपेक्षित एंटिटी / Expected Entities | वास्तविक एंटिटी / Actual Entities | स्थिति / Status |
|----|---------------------------|----------------------------------|--------------------------------|---------------|
| EE-EN-001 | Send "Update stock of basmati rice to 75 kg" | name: "basmati rice", stock: 75 | | |
| EE-EN-002 | Send "Add new product toor dal price 120 stock 30" | name: "toor dal", price: 120, stock: 30 | | |
| EE-EN-003 | Send "Show items with stock below 10" | threshold: 10 | | |
| EE-EN-004 | Send "Show report from 1st June to 30th June" | start_date: "2023-06-01", end_date: "2023-06-30" | | |
| EE-EN-005 | Send "Show top 5 products this month" | limit: 5, time_range: "this_month" | | |

### हिंदी एंटिटी निष्कर्षण / Hindi Entity Extraction

| ID | परीक्षण मामला / Test Case | अपेक्षित एंटिटी / Expected Entities | वास्तविक एंटिटी / Actual Entities | स्थिति / Status |
|----|---------------------------|----------------------------------|--------------------------------|---------------|
| EE-HI-001 | Send "बासमती चावल का स्टॉक 75 किलो करो" | name: "बासमती चावल", stock: 75 | | |
| EE-HI-002 | Send "नया प्रोडक्ट तूर दाल जोड़ो कीमत 120 स्टॉक 30" | name: "तूर दाल", price: 120, stock: 30 | | |
| EE-HI-003 | Send "10 से कम स्टॉक वाले आइटम दिखाओ" | threshold: 10 | | |
| EE-HI-004 | Send "1 जून से 30 जून तक की रिपोर्ट दिखाओ" | start_date: "2023-06-01", end_date: "2023-06-30" | | |
| EE-HI-005 | Send "इस महीने के टॉप 5 प्रोडक्ट दिखाओ" | limit: 5, time_range: "this_month" | | |

## प्रतिक्रिया उत्पादन परीक्षण / Response Generation Testing

### अंग्रेजी प्रतिक्रिया / English Responses

| ID | परीक्षण मामला / Test Case | अपेक्षित प्रतिक्रिया / Expected Response | वास्तविक प्रतिक्रिया / Actual Response | स्थिति / Status |
|----|---------------------------|--------------------------------------|----------------------------------|---------------|
| RG-EN-001 | Send "Show my inventory" | Properly formatted inventory list in English | | |
| RG-EN-002 | Send "Update stock of rice to 50" | Confirmation message in English | | |
| RG-EN-003 | Send "Show low stock items" | List of low stock items in English | | |
| RG-EN-004 | Send "Show report for today" | Today's report in English | | |
| RG-EN-005 | Send "I don't understand" | Appropriate error message in English | | |

### हिंदी प्रतिक्रिया / Hindi Responses

| ID | परीक्षण मामला / Test Case | अपेक्षित प्रतिक्रिया / Expected Response | वास्तविक प्रतिक्रिया / Actual Response | स्थिति / Status |
|----|---------------------------|--------------------------------------|----------------------------------|---------------|
| RG-HI-001 | Send "मेरा इन्वेंटरी दिखाओ" | Properly formatted inventory list in Hindi | | |
| RG-HI-002 | Send "चावल का स्टॉक 50 करो" | Confirmation message in Hindi | | |
| RG-HI-003 | Send "कम स्टॉक वाले आइटम दिखाओ" | List of low stock items in Hindi | | |
| RG-HI-004 | Send "आज की रिपोर्ट दिखाओ" | Today's report in Hindi | | |
| RG-HI-005 | Send "मुझे समझ नहीं आया" | Appropriate error message in Hindi | | |

## भाषा स्विचिंग परीक्षण / Language Switching Testing

| ID | परीक्षण मामला / Test Case | अपेक्षित परिणाम / Expected Result | वास्तविक परिणाम / Actual Result | स्थिति / Status |
|----|---------------------------|--------------------------------|------------------------------|---------------|
| LS-001 | Send "Switch to Hindi" followed by an English command | Response in Hindi | | |
| LS-002 | Send "हिंदी में बदलो" followed by a Hindi command | Response in Hindi | | |
| LS-003 | Send "अंग्रेजी में बदलो" followed by a Hindi command | Response in English | | |
| LS-004 | Send "Switch to English" followed by an English command | Response in English | | |
| LS-005 | Send "Reply in Hindi" followed by an English command | Response in Hindi | | |
| LS-006 | Send "हिंदी में जवाब दो" followed by an English command | Response in Hindi | | |

## त्रुटि प्रबंधन परीक्षण / Error Handling Testing

### अंग्रेजी त्रुटि प्रबंधन / English Error Handling

| ID | परीक्षण मामला / Test Case | अपेक्षित प्रतिक्रिया / Expected Response | वास्तविक प्रतिक्रिया / Actual Response | स्थिति / Status |
|----|---------------------------|--------------------------------------|----------------------------------|---------------|
| EH-EN-001 | Send "Update stock of" (incomplete command) | Ask for product name and quantity | | |
| EH-EN-002 | Send "Add new product" (incomplete command) | Ask for product details | | |
| EH-EN-003 | Send "abcxyz" (nonsense command) | Appropriate error message | | |
| EH-EN-004 | Send "Delete all products" (unsupported command) | Explain that this operation is not supported | | |
| EH-EN-005 | Send "What is the price of rice?" (ambiguous intent) | Ask for clarification | | |

### हिंदी त्रुटि प्रबंधन / Hindi Error Handling

| ID | परीक्षण मामला / Test Case | अपेक्षित प्रतिक्रिया / Expected Response | वास्तविक प्रतिक्रिया / Actual Response | स्थिति / Status |
|----|---------------------------|--------------------------------------|----------------------------------|---------------|
| EH-HI-001 | Send "स्टॉक अपडेट करो" (incomplete command) | Ask for product name and quantity in Hindi | | |
| EH-HI-002 | Send "नया प्रोडक्ट जोड़ो" (incomplete command) | Ask for product details in Hindi | | |
| EH-HI-003 | Send "अबकडहज" (nonsense command) | Appropriate error message in Hindi | | |
| EH-HI-004 | Send "सभी प्रोडक्ट हटा दो" (unsupported command) | Explain that this operation is not supported in Hindi | | |
| EH-HI-005 | Send "चावल का दाम क्या है?" (ambiguous intent) | Ask for clarification in Hindi | | |

## वाक्यविन्यास और व्याकरण परीक्षण / Syntax and Grammar Testing

### हिंदी वाक्यविन्यास / Hindi Syntax

| ID | परीक्षण मामला / Test Case | अपेक्षित परिणाम / Expected Result | वास्तविक परिणाम / Actual Result | स्थिति / Status |
|----|---------------------------|--------------------------------|------------------------------|---------------|
| SG-HI-001 | Check response for "मेरा इन्वेंटरी दिखाओ" | Grammatically correct Hindi | | |
| SG-HI-002 | Check response for "चावल का स्टॉक 50 करो" | Proper use of postpositions (का, के, की) | | |
| SG-HI-003 | Check response for "आज की रिपोर्ट भेजो" | Correct verb conjugation | | |
| SG-HI-004 | Check response for "कम स्टॉक वाले आइटम दिखाओ" | Correct use of adjectives | | |
| SG-HI-005 | Check error message in Hindi | Natural sounding error message | | |

## संदर्भ और बातचीत परीक्षण / Context and Conversation Testing

| ID | परीक्षण मामला / Test Case | अपेक्षित परिणाम / Expected Result | वास्तविक परिणाम / Actual Result | स्थिति / Status |
|----|---------------------------|--------------------------------|------------------------------|---------------|
| CC-001 | Send "Show my inventory" then "Update rice to 50" | Understand that "rice" refers to a product | | |
| CC-002 | Send "मेरा इन्वेंटरी दिखाओ" then "चावल 50 करो" | Understand that "चावल" refers to a product | | |
| CC-003 | Start in English, switch to Hindi, then back to English | Maintain context across language switches | | |
| CC-004 | Ask "What are my low stock items?" then "Order more of these" | Understand the reference to low stock items | | |
| CC-005 | Ask "कौन से आइटम कम हैं?" then "इनको और ऑर्डर करो" | Understand the reference to low stock items | | |

## क्षेत्रीय बोली परीक्षण / Regional Dialect Testing

| ID | परीक्षण मामला / Test Case | अपेक्षित परिणाम / Expected Result | वास्तविक परिणाम / Actual Result | स्थिति / Status |
|----|---------------------------|--------------------------------|------------------------------|---------------|
| RD-001 | Send "चावल का स्टाक 50 कर दो" (स्टॉक instead of स्टाक) | Recognize "स्टाक" as "स्टॉक" | | |
| RD-002 | Send "आटा कितना बचा है" (colloquial for inventory check) | Recognize as inventory query | | |
| RD-003 | Send "दाल खतम हो गई" (colloquial for low stock) | Recognize as low stock notification | | |
| RD-004 | Send "माल कितना बिका आज" (colloquial for sales report) | Recognize as report request | | |
| RD-005 | Send "ग्राहक कौन-कौन आए" (colloquial for customer data) | Recognize as customer data request | | |

## लिप्यंतरण परीक्षण / Transliteration Testing

| ID | परीक्षण मामला / Test Case | अपेक्षित परिणाम / Expected Result | वास्तविक परिणाम / Actual Result | स्थिति / Status |
|----|---------------------------|--------------------------------|------------------------------|---------------|
| TR-001 | Send "mera inventory dikhao" (Hindi in Roman script) | Recognize as Hindi command | | |
| TR-002 | Send "chawal ka stock 50 karo" (Hindi in Roman script) | Recognize as Hindi command | | |
| TR-003 | Send "kam stock wale item dikhao" (Hindi in Roman script) | Recognize as Hindi command | | |
| TR-004 | Send "aaj ki report bhejo" (Hindi in Roman script) | Recognize as Hindi command | | |
| TR-005 | Send "naya product add karo" (Hindi in Roman script) | Recognize as Hindi command | | |

## परीक्षण निष्कर्ष / Testing Conclusion

### समस्याओं का सारांश / Summary of Issues

| ID | समस्या विवरण / Issue Description | गंभीरता / Severity | प्राथमिकता / Priority | स्थिति / Status |
|----|----------------------------------|-------------------|---------------------|---------------|
|    |                                  |                   |                     |               |
|    |                                  |                   |                     |               |
|    |                                  |                   |                     |               |

### सुधार के सुझाव / Improvement Suggestions

1. 
2. 
3. 

### परीक्षक की टिप्पणियां / Tester Comments



### परीक्षण अनुमोदन / Test Approval

**परीक्षक / Tester:** ___________________________ **तिथि / Date:** _______________

**अनुमोदनकर्ता / Approver:** ___________________________ **तिथि / Date:** _______________