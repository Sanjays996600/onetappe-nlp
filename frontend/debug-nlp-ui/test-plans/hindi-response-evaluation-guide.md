# Hindi & Hinglish Response Evaluation Guide

## Overview
This guide provides criteria for evaluating the quality of WhatsApp bot responses in Hindi (Devanagari) and Hinglish (Romanized Hindi). It is designed to help testers assess linguistic accuracy, contextual correctness, and user-friendliness of multilingual responses.

## Evaluation Criteria

### 1. Language Accuracy

#### Hindi (Devanagari) Evaluation

| Aspect | Pass Criteria | Fail Criteria | Examples |
|--------|--------------|---------------|----------|
| Grammar | Correct verb forms, gender agreement, postpositions | Incorrect verb conjugation, wrong gender agreement | ✅ "आपका ऑर्डर भेज दिया गया है" <br> ❌ "आपका ऑर्डर भेज दिया गया हैं" |
| Spelling | Standard Hindi spelling | Misspelled words, incorrect use of मात्रा (vowel marks) | ✅ "आपका इन्वेंटरी" <br> ❌ "आपका इनवेंटरी" |
| Sentence Structure | Natural Hindi sentence flow | Direct English-to-Hindi translation structure | ✅ "आपके पास 5 प्रोडक्ट्स हैं" <br> ❌ "आप हैं 5 प्रोडक्ट्स" |
| Technical Terms | Consistent use of Hindi or English technical terms | Inconsistent switching between Hindi and English terms | ✅ "आपका इन्वेंटरी खाली है" (consistent) <br> ❌ "आपका स्टॉक खाली है लेकिन इन्वेंटरी में 5 आइटम हैं" (inconsistent) |

#### Hinglish (Romanized Hindi) Evaluation

| Aspect | Pass Criteria | Fail Criteria | Examples |
|--------|--------------|---------------|----------|
| Spelling Consistency | Consistent romanization style | Inconsistent spelling of the same Hindi words | ✅ "aapka order" (consistent) <br> ❌ "aapka order" then "apka order" (inconsistent) |
| Grammar | Natural Hinglish grammar patterns | Awkward mixing of English and Hindi grammar | ✅ "aapka order ready hai" <br> ❌ "aapka order is ready" |
| Readability | Easy to read and understand | Confusing transliteration | ✅ "stock update ho gaya hai" <br> ❌ "stak updt ho gya h" |
| Tone | Conversational Hinglish | Overly formal or overly casual | ✅ "aapka order taiyar hai" <br> ❌ "order ready h, le jao" |

### 2. Contextual Correctness

| Aspect | Pass Criteria | Fail Criteria | Examples |
|--------|--------------|---------------|----------|
| Intent Understanding | Response matches user's intent | Response addresses wrong intent | ✅ User: "मेरा स्टॉक दिखाओ" → Bot shows inventory <br> ❌ User: "मेरा स्टॉक दिखाओ" → Bot shows orders |
| Entity Recognition | Correctly identifies entities (products, dates, numbers) | Misses or misidentifies entities | ✅ User: "चावल का स्टॉक अपडेट करो" → Bot updates rice stock <br> ❌ User: "चावल का स्टॉक अपडेट करो" → Bot doesn't recognize "चावल" (rice) |
| Context Retention | Maintains context in conversation | Loses context between messages | ✅ User: "मेरे ऑर्डर दिखाओ" → Bot: "कौन सा ऑर्डर?" → User: "सबसे नया" → Bot shows newest order <br> ❌ User: "मेरे ऑर्डर दिखाओ" → Bot: "कौन सा ऑर्डर?" → User: "सबसे नया" → Bot doesn't understand |

### 3. User-Friendliness

| Aspect | Pass Criteria | Fail Criteria | Examples |
|--------|--------------|---------------|----------|
| Clarity | Clear, unambiguous responses | Confusing or vague responses | ✅ "आपके पास 5 प्रोडक्ट हैं जिनका स्टॉक कम है" <br> ❌ "कुछ प्रोडक्ट कम हैं" |
| Brevity | Concise responses | Unnecessarily verbose responses | ✅ "ऑर्डर #123 अपडेट हो गया" <br> ❌ "आपके द्वारा अनुरोधित ऑर्डर नंबर 123 का स्टेटस अपडेट कर दिया गया है और अब यह सिस्टम में अपडेट हो चुका है" |
| Helpfulness | Provides useful information or clear next steps | Unhelpful or dead-end responses | ✅ "स्टॉक अपडेट नहीं हुआ। कृपया प्रोडक्ट नाम और मात्रा दोबारा भेजें" <br> ❌ "स्टॉक अपडेट नहीं हुआ" (no guidance) |
| Tone | Polite, helpful, professional | Rude, confusing, or overly formal/informal | ✅ "आपका ऑर्डर तैयार है" <br> ❌ "ऑर्डर रेडी है, ले जाओ" (too casual) |

### 4. Cultural Appropriateness

| Aspect | Pass Criteria | Fail Criteria | Examples |
|--------|--------------|---------------|----------|
| Formality Level | Appropriate level of formality (आप vs तुम) | Inconsistent or inappropriate formality | ✅ Consistent use of "आप" for customers <br> ❌ Mixing "आप" and "तुम" in the same conversation |
| Idioms & Expressions | Natural Hindi expressions when appropriate | Direct translation of English idioms | ✅ "चिंता मत कीजिए" <br> ❌ "चिंता न लें" (direct translation of "don't worry") |
| Regional Sensitivity | Neutral Hindi that works across regions | Region-specific terms without explanation | ✅ "दाल" (universally understood) <br> ❌ Region-specific terms like "अरहर" without clarification |

## Common Issues to Watch For

### 1. Mixed Language Problems

- **Code-switching**: Inconsistent switching between Hindi and English
  - Example: "आपका order process हो गया है और delivery जल्द होगी"
  - Better: "आपका ऑर्डर प्रोसेस हो गया है और डिलीवरी जल्द होगी" (consistent transliteration)

- **Inconsistent Technical Terms**: Using different terms for the same concept
  - Example: Using both "स्टॉक" and "इन्वेंटरी" interchangeably
  - Better: Choose one term and use consistently

### 2. Translation Issues

- **Word-for-word Translation**: Direct translation that sounds unnatural
  - Example: "हम आपकी सहायता के लिए यहां हैं" (We are here to help you) - sounds translated
  - Better: "हम आपकी मदद के लिए मौजूद हैं" (more natural Hindi)

- **Missing Cultural Context**: Translations that miss cultural nuances
  - Example: "Have a good day" → "एक अच्छा दिन है" (literal translation)
  - Better: "शुभ दिन" or "अच्छा दिन हो"

### 3. Technical Limitations

- **Entity Recognition Failures**: System fails to recognize Hindi entities
  - Example: Not recognizing "चावल" as a product name

- **Handling of Hindi Numbers**: Issues with Hindi numerals or number words
  - Example: Not understanding "दो किलो चावल" (two kilos of rice)

## Response Quality Scoring

Use this scoring system to evaluate overall response quality:

| Score | Description | Criteria |
|-------|-------------|----------|
| 5 | Excellent | Perfect grammar, natural phrasing, completely appropriate, helpful |
| 4 | Good | Minor grammar issues, mostly natural, appropriate, helpful |
| 3 | Acceptable | Some grammar or phrasing issues, but understandable and helpful |
| 2 | Poor | Significant grammar issues, unnatural phrasing, somewhat helpful |
| 1 | Unacceptable | Major grammar problems, confusing, inappropriate, or unhelpful |

## Testing Tips

1. **Test with Real-world Variations**:
   - Test with different ways of saying the same thing
   - Include common misspellings and regional variations

2. **Compare Across Languages**:
   - Test the same intent in English, Hindi, and Hinglish
   - Note any discrepancies in quality or understanding

3. **Focus on Edge Cases**:
   - Mixed language inputs
   - Grammatically incorrect but understandable inputs
   - Regional dialects and slang

4. **Document Specific Issues**:
   - Note specific words or phrases that cause problems
   - Identify patterns in misunderstandings

## Recommended Improvements Template

When identifying issues, document them in this format:

```
Issue Type: [Grammar/Translation/Entity Recognition/etc.]
Command: [Original command]
Current Response: [What the system currently returns]
Issue Description: [Specific problem with the response]
Recommended Response: [How the response should be improved]
Priority: [High/Medium/Low]
```

---

*This guide should be used alongside the Multilingual WhatsApp Command Testing Plan and Test Results Template.*