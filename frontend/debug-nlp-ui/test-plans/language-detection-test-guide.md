# Language Detection Testing Guide

## Overview

This guide focuses specifically on testing the language detection capabilities of the WhatsApp chatbot across English, Hindi (Devanagari), and Hinglish (Romanized Hindi). Accurate language detection is crucial for proper intent recognition and appropriate response generation.

## Language Detection Test Categories

### 1. Pure Language Tests

These tests verify that the system correctly identifies commands in a single, clearly defined language.

#### English
- Simple commands: "Show inventory"
- Complex commands: "Generate a sales report for the period between March 1 and March 15"
- Business terminology: "Check the ROI for product XYZ"

#### Hindi (Devanagari)
- Simple commands: "इन्वेंटरी दिखाओ"
- Complex commands: "1 मार्च से 15 मार्च तक की बिक्री रिपोर्ट बनाएं"
- Regional variations: Test with different regional Hindi dialects

#### Hinglish (Romanized Hindi)
- Simple commands: "Inventory dikhao"
- Complex commands: "1 March se 15 March tak ki sales report banao"
- Spelling variations: "Inventry dikhao" vs "Inventory dikhao"

### 2. Mixed Language Tests

These tests verify how the system handles commands that mix multiple languages.

#### English-Hindi Mix
- Hindi words in English sentences: "Show my इन्वेंटरी"
- English words in Hindi sentences: "मेरा inventory दिखाओ"
- Equal mix: "मेरा inventory कब update होगा?"

#### English-Hinglish Mix
- Hinglish words in English sentences: "Show my inventory ka status"
- English words in Hinglish sentences: "Mera inventory update karo with new prices"
- Equal mix: "Order status kya hai for customer John?"

#### Hindi-Hinglish Mix
- Hinglish words in Hindi sentences: "मेरा stock kitna है?"
- Hindi words in Hinglish sentences: "Mera स्टॉक kitna hai?"
- Script switching: "मेरा stock कितना hai?"

### 3. Ambiguous Language Tests

These tests check how the system handles commands where language detection is challenging.

#### Shared Vocabulary
- Words common to multiple languages: "order status" (could be English or Hinglish)
- Brand names and product codes: "XYZ123 ka price update karo"
- Numbers and dates: "12/05/2023 ka report"

#### Short Commands
- Single word commands: "Inventory", "स्टॉक", "Report"
- Two-word commands: "Show inventory", "रिपोर्ट दिखाओ", "Report dikhao"
- Abbreviations: "inv", "rpt", "ord"

### 4. Regional Variation Tests

These tests verify how the system handles regional language variations.

#### Hindi Regional Variations
- Eastern Hindi: "हमर इन्वेंटरी देखावा"
- Western Hindi: "म्हारो इन्वेंटरी दिखाओ"
- Standard Hindi with regional vocabulary: "इन्वेंटरी में कितना माल है?"

#### Hinglish Regional Variations
- Northern style: "Inventory dikha do"
- Mumbai style: "Inventory dikha na"
- Southern influence: "Inventory dikhao please"

### 5. Code-Switching Pattern Tests

These tests check how the system handles different patterns of switching between languages.

#### Inter-sentential Switching
- Multiple sentences in different languages: "Show inventory. बिक्री रिपोर्ट भी दिखाओ।"
- Questions and answers in different languages: "Inventory kahan hai? Show it to me."

#### Intra-sentential Switching
- Mid-sentence language change: "Show me the inventory जो कल अपडेट किया था"
- Phrase-level switching: "मेरे last month के orders का status बताओ"
- Word-level switching: "मेरे inventory में kitne products हैं?"

### 6. Edge Case Tests

These tests verify how the system handles unusual language patterns.

#### Typos and Misspellings
- English typos: "Show my inevntory"
- Hindi typos: "इनवेंटरी दिखाओ"
- Hinglish typos: "Inventry dikhao"

#### Mixed Scripts
- Roman script for Hindi words: "Mera stock dikhao"
- Devanagari for English words: "मेरा इन्वेंटरी शो करो"
- Mixed script in single words: "in वेंटरी"

#### Emojis and Special Characters
- Commands with emojis: "📦 inventory dikhao"
- Special characters: "#inventory", "@order status"
- Punctuation variations: "inventory?", "inventory!", "inventory..."

## Testing Methodology

### Test Process

1. **Preparation:**
   - Create a spreadsheet with columns for: Test ID, Command, Expected Language, Detected Language, Confidence Score, Pass/Fail, Notes
   - Group tests by category for easier analysis

2. **Execution:**
   - Enter each test command exactly as specified
   - Record the detected language and confidence score
   - Mark as Pass if the detected language matches the expected language, Fail if not
   - Add notes about any interesting observations

3. **Analysis:**
   - Calculate pass rate for each language and category
   - Identify patterns in failures
   - Note any confidence score thresholds that seem to correlate with accuracy

### Common Issues to Look For

1. **Misclassification Patterns:**
   - Hindi consistently misclassified as Hinglish or vice versa
   - Short commands consistently misclassified
   - Certain vocabulary triggering incorrect classification

2. **Confidence Score Issues:**
   - Low confidence scores for correct classifications
   - High confidence scores for incorrect classifications
   - Inconsistent confidence scores for similar commands

3. **Mixed Language Handling:**
   - Always defaulting to one language for mixed content
   - Inconsistent handling of similar mixing patterns
   - Threshold for language dominance in mixed content

4. **Regional Variation Issues:**
   - Inability to recognize certain regional variations
   - Misclassification of regional variations

## Reporting Format

### Summary Table

| Category | Total Tests | Pass | Fail | Pass Rate |
|----------|-------------|------|------|----------|
| Pure English | | | | |
| Pure Hindi | | | | |
| Pure Hinglish | | | | |
| Mixed Language | | | | |
| Ambiguous Language | | | | |
| Regional Variations | | | | |
| Code-Switching | | | | |
| Edge Cases | | | | |
| **Overall** | | | | |

### Detailed Findings

For each failed test, provide:

1. **Test ID and Command:** The specific test that failed
2. **Expected vs. Actual:** What language was expected vs. what was detected
3. **Confidence Score:** The confidence score reported by the system
4. **Pattern:** Any pattern this failure seems to be part of
5. **Impact:** How this might affect user experience
6. **Recommendation:** Suggested fix or improvement

## Improvement Recommendations

Based on test results, consider recommending:

1. **Training Data Enhancements:**
   - More examples of specific mixing patterns
   - More regional variations
   - More examples of edge cases

2. **Algorithm Adjustments:**
   - Adjusting confidence thresholds
   - Improving handling of mixed language content
   - Better handling of short commands

3. **User Experience Improvements:**
   - Explicit language selection option
   - Confirmation for ambiguous cases
   - Improved error messages for language detection issues

## Test Schedule

1. **Day 1:** Pure language tests (English, Hindi, Hinglish)
2. **Day 2:** Mixed language tests
3. **Day 3:** Ambiguous language and regional variation tests
4. **Day 4:** Code-switching pattern tests
5. **Day 5:** Edge case tests

## Conclusion

Thorough testing of language detection capabilities is essential for ensuring a good user experience in a multilingual chatbot. By systematically testing various language patterns and edge cases, you can identify issues and patterns that will help improve the overall quality of the chatbot's language understanding.

---

*This document should be used alongside the Multilingual WhatsApp Command Testing Plan and Test Case Matrix.*