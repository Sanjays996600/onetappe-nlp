# Common Language Issues and Solutions in WhatsApp Chatbot Responses

## Overview
This document catalogs common linguistic issues that may arise in multilingual WhatsApp chatbot responses and provides recommended solutions. It serves as a reference for testers to identify, classify, and report problems consistently.

## Hindi (Devanagari) Common Issues

### 1. Gender Agreement Issues

**Problem:** Incorrect gender agreement between nouns and verbs/adjectives.

**Examples:**
- ❌ "आपका ऑर्डर भेजा गई है" (Incorrect: masculine noun with feminine verb form)
- ✅ "आपका ऑर्डर भेजा गया है" (Correct: masculine noun with masculine verb form)

**Solution:** Ensure proper gender agreement based on the noun's gender. Common nouns like "ऑर्डर" (order), "प्रोडक्ट" (product), and "इन्वेंटरी" (inventory) are typically masculine in Hindi.

### 2. Postposition Errors

**Problem:** Incorrect use of postpositions (का, के, की, में, पर, etc.)

**Examples:**
- ❌ "स्टॉक का अपडेट" (Incorrect when referring to updating the stock)
- ✅ "स्टॉक में अपडेट" (Correct when referring to updating in the stock)

**Solution:** Review and correct postposition usage based on the relationship between words and the intended meaning.

### 3. Transliteration Issues

**Problem:** Inconsistent transliteration of English terms into Hindi script.

**Examples:**
- ❌ Mixed usage: "आपका ऑर्डर" and "आपका आर्डर" in the same conversation
- ✅ Consistent usage: "आपका ऑर्डर" throughout

**Solution:** Maintain a glossary of standardized transliterations for common terms and ensure consistent usage.

### 4. Formal/Informal Mixing

**Problem:** Inconsistent levels of formality within the same response.

**Examples:**
- ❌ "आप का ऑर्डर तैयार है। तुम्हारा बिल 500 रुपये है।" (Mixes formal "आप" with informal "तुम")
- ✅ "आप का ऑर्डर तैयार है। आपका बिल 500 रुपये है।" (Consistently formal)

**Solution:** Maintain consistent formality level throughout responses, preferably using the formal "आप" form for business communications.

### 5. Honorific Consistency

**Problem:** Inconsistent use of honorifics and respectful forms.

**Examples:**
- ❌ "कृपया अपना ऑर्डर चेक कर। धन्यवाद।" (Missing honorific suffix)
- ✅ "कृपया अपना ऑर्डर चेक करें। धन्यवाद।" (Proper honorific form)

**Solution:** Consistently use honorific forms (करें instead of कर, बताएं instead of बताओ) in customer communications.

## Hinglish (Romanized Hindi) Common Issues

### 1. Inconsistent Romanization

**Problem:** Multiple ways of spelling the same Hindi words in Roman script.

**Examples:**
- ❌ Mixed usage: "aapka" and "apka" for "आपका" in the same conversation
- ✅ Consistent usage: "aapka" throughout

**Solution:** Standardize Romanization patterns for common words and phrases.

### 2. Grammar Structure Confusion

**Problem:** Mixing English and Hindi grammar structures incorrectly.

**Examples:**
- ❌ "Order ka status check karo" (Hindi structure) vs "Check the order status" (English structure)
- ✅ "Order ka status check karein" (Consistent Hindi structure with respectful form)

**Solution:** Maintain consistent grammatical structure based on the primary language of the sentence.

### 3. Code-Switching Issues

**Problem:** Awkward or confusing switches between Hindi and English within a sentence.

**Examples:**
- ❌ "Aapka order has been shipped aur delivery expected hai by tomorrow"
- ✅ "Aapka order ship kar diya gaya hai aur delivery kal tak expected hai"

**Solution:** Make code-switching more natural by maintaining consistent grammatical structure and avoiding mid-phrase switches.

### 4. Formality Inconsistency

**Problem:** Mixing formal and informal address forms.

**Examples:**
- ❌ "Aap apna order check karo" (Mixes formal "Aap" with informal "karo")
- ✅ "Aap apna order check karein" (Consistently formal)

**Solution:** Maintain consistent formality level, using "karein" instead of "karo" when addressing customers formally.

### 5. Punctuation and Spacing

**Problem:** Inconsistent or incorrect punctuation and spacing in Romanized text.

**Examples:**
- ❌ "ordercancel hogaya hai"
- ✅ "Order cancel ho gaya hai"

**Solution:** Use proper spacing between words and consistent capitalization patterns.

## English Common Issues

### 1. Indian English Expressions

**Problem:** Using Indian English expressions that may not be universally understood.

**Examples:**
- ❌ "Please do the needful for your order"
- ✅ "Please take the necessary action for your order"

**Solution:** Use standard English expressions while maintaining clarity.

### 2. Tense Consistency

**Problem:** Inconsistent use of tenses within responses.

**Examples:**
- ❌ "Your order has been shipped and will be delivered yesterday"
- ✅ "Your order has been shipped and will be delivered tomorrow"

**Solution:** Review responses for logical tense consistency.

### 3. Article Usage

**Problem:** Missing or incorrect articles (a, an, the).

**Examples:**
- ❌ "Please check inventory for update"
- ✅ "Please check the inventory for an update"

**Solution:** Review and correct article usage according to standard English grammar.

## Cross-Language Issues

### 1. Translation Inconsistency

**Problem:** The same concept is expressed differently across languages.

**Examples:**
- English: "Your order has been cancelled"
- Hindi: "आपका ऑर्डर रद्द हो गया है" (passive voice)
- Hinglish: "Humne aapka order cancel kar diya hai" (active voice)

**Solution:** Maintain consistent voice and structure across language versions when possible.

### 2. Feature Name Consistency

**Problem:** Inconsistent translation of product features and commands.

**Examples:**
- English: "low stock alert"
- Hindi: sometimes "कम स्टॉक अलर्ट" and sometimes "स्टॉक कम होने की सूचना"

**Solution:** Create and maintain a glossary of standardized translations for product features, commands, and technical terms.

### 3. Tone Shifts Across Languages

**Problem:** Different levels of formality or friendliness across languages.

**Examples:**
- English: Casual and friendly
- Hindi: Overly formal and stiff

**Solution:** Define a consistent tone guide for all languages that aligns with the One Tappe brand voice.

## Response Structure Issues

### 1. Inconsistent Information Order

**Problem:** The order of information varies across responses.

**Examples:**
- Some responses put the status first: "Cancelled: Your order #12345..."
- Others put the order number first: "Order #12345 has been cancelled..."

**Solution:** Standardize information hierarchy and structure across all responses.

### 2. Greeting and Closing Inconsistency

**Problem:** Inconsistent use of greetings and closings.

**Examples:**
- Some responses include "Thank you" while others don't
- Inconsistent use of customer name in greetings

**Solution:** Create templates with consistent greeting and closing patterns.

## Testing and Reporting Guidelines

### How to Report Issues

1. **Be Specific:** Identify the exact word, phrase, or structure that is problematic
2. **Provide Context:** Include the full response and the command that triggered it
3. **Suggest Correction:** When possible, suggest a corrected version
4. **Classify Issue Type:** Use the categories in this document to classify the issue
5. **Rate Severity:** Indicate whether the issue is:
   - Critical (prevents understanding)
   - Major (significantly impacts clarity)
   - Minor (noticeable but doesn't impact understanding)

### Example Issue Report

```
Command: "stock update karo"
Detected Language: Hinglish
Response: "Stock update ho gaya hai. Aap check karo inventory page par."

Issue: Formality Inconsistency
Description: Uses informal "karo" with formal customer address
Severity: Minor
Suggested Correction: "Stock update ho gaya hai. Aap inventory page par check karein."
```

## Continuous Improvement Process

1. **Collect Issues:** Gather all language issues identified during testing
2. **Categorize:** Group issues by language and type
3. **Prioritize:** Focus on high-severity issues first
4. **Update Guidelines:** Refine language guidelines based on common issues
5. **Create Training Data:** Use examples of issues to improve NLP training
6. **Retest:** Verify fixes and improvements in subsequent testing rounds

---

*This document should be used alongside the Multilingual WhatsApp Command Testing Plan and related documents.*