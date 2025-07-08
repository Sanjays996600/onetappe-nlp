# Confidence Score Analysis Guide

## Overview

This guide provides a framework for analyzing confidence scores in the WhatsApp chatbot's intent recognition across English, Hindi (Devanagari), and Hinglish (Romanized Hindi). Understanding confidence score patterns is crucial for improving the chatbot's accuracy and reliability.

## Confidence Score Benchmarks

### Interpretation Scale

| Confidence Score Range | Interpretation | Action |
|------------------------|----------------|--------|
| 0.90 - 1.00 | Very High Confidence | Proceed with response |
| 0.75 - 0.89 | High Confidence | Proceed with response |
| 0.50 - 0.74 | Moderate Confidence | Proceed with caution, consider clarification |
| 0.30 - 0.49 | Low Confidence | Consider asking for clarification |
| 0.00 - 0.29 | Very Low Confidence | Ask for clarification or reformulation |

### Expected Benchmarks by Command Type

| Command Type | Expected Minimum Score | Notes |
|--------------|------------------------|-------|
| Simple, common commands | 0.80+ | E.g., "Show inventory", "इन्वेंटरी दिखाओ" |
| Complex commands | 0.65+ | E.g., "Generate report from March 1 to March 15" |
| Commands with parameters | 0.70+ | E.g., "Update product XYZ to 50 units" |
| Ambiguous commands | 0.40+ | E.g., "Check status" (could mean multiple things) |
| Commands with typos | 0.60+ | E.g., "Show inevntory" |

## Testing Methodology

### 1. Baseline Testing

Establish baseline confidence scores for standard commands in each language:

1. **Select representative commands:** Choose 5-10 standard commands for each intent
2. **Test in all languages:** Test each command in English, Hindi, and Hinglish
3. **Record baseline scores:** Document the confidence scores for each
4. **Calculate averages:** Determine average confidence by language and intent

#### Baseline Testing Template

| Command | Language | Intent | Confidence Score | Notes |
|---------|----------|--------|------------------|-------|
| "Show inventory" | English | GetInventory | | |
| "इन्वेंटरी दिखाओ" | Hindi | GetInventory | | |
| "Inventory dikhao" | Hinglish | GetInventory | | |

### 2. Variation Testing

Test how variations of the same command affect confidence scores:

1. **Word order variations:** E.g., "Show me inventory" vs "Inventory show me"
2. **Formality variations:** E.g., "इन्वेंटरी दिखाओ" vs "इन्वेंटरी दिखाइए"
3. **Length variations:** Short vs long versions of the same command
4. **Vocabulary variations:** Different words for the same concept

#### Variation Testing Template

| Base Command | Variation | Language | Intent | Confidence Score | Score Difference | Notes |
|-------------|-----------|----------|--------|------------------|------------------|-------|
| "Show inventory" | "Inventory show" | English | GetInventory | | | |
| "इन्वेंटरी दिखाओ" | "दिखाओ इन्वेंटरी" | Hindi | GetInventory | | | |

### 3. Cross-Language Testing

Analyze how confidence scores vary across languages for the same intent:

1. **Direct translations:** Compare scores for direct translations
2. **Cultural adaptations:** Compare scores for culturally adapted versions
3. **Language-specific features:** Identify features that affect scores in specific languages

#### Cross-Language Comparison Template

| Intent | English Command | English Score | Hindi Command | Hindi Score | Hinglish Command | Hinglish Score | Notes |
|--------|----------------|---------------|---------------|-------------|------------------|----------------|-------|
| GetInventory | "Show inventory" | | "इन्वेंटरी दिखाओ" | | "Inventory dikhao" | | |

### 4. Edge Case Testing

Test how edge cases affect confidence scores:

1. **Typos and misspellings:** E.g., "Show inevntory"
2. **Mixed language:** E.g., "Show मेरा inventory"
3. **Abbreviated text:** E.g., "inv dikhao"
4. **Commands with emojis:** E.g., "📦 inventory dikhao"
5. **Ambiguous commands:** E.g., "check status"

#### Edge Case Testing Template

| Edge Case Type | Command | Language | Expected Intent | Actual Intent | Confidence Score | Notes |
|----------------|---------|----------|----------------|--------------|------------------|-------|
| Typo | "Show inevntory" | English | GetInventory | | | |
| Mixed Language | "Show मेरा inventory" | Mixed | GetInventory | | | |

## Analysis Patterns to Look For

### 1. Language-Specific Patterns

- **Consistent differences:** Does one language consistently score higher/lower?
- **Intent-specific differences:** Are certain intents recognized better in specific languages?
- **Threshold differences:** Should different thresholds be used for different languages?

### 2. Command Structure Patterns

- **Length impact:** How does command length affect confidence?
- **Parameter impact:** How do parameters (product names, dates, etc.) affect confidence?
- **Word order sensitivity:** How sensitive is the system to word order changes?

### 3. Error Patterns

- **False positives:** High confidence for incorrect intents
- **False negatives:** Low confidence for correct intents
- **Confusion patterns:** Specific intents frequently confused with others

### 4. Improvement Opportunities

- **Training gaps:** Command patterns with consistently low scores
- **Threshold adjustments:** Potential for language-specific thresholds
- **Intent refinement:** Overlapping intents that cause confusion

## Issue Classification

### 1. Critical Issues

- High confidence (>0.80) for incorrect intent
- Very low confidence (<0.30) for common, correctly formatted commands
- Consistent failure to recognize specific intents in specific languages

### 2. Major Issues

- Moderate confidence (0.50-0.79) for incorrect intent
- Low confidence (0.30-0.49) for common, correctly formatted commands
- Significant disparity (>0.20) in scores across languages for the same intent

### 3. Minor Issues

- Slight disparity (0.10-0.19) in scores across languages
- Moderate confidence (0.50-0.79) for edge cases
- Inconsistent scores for similar command variations

## Improvement Recommendations

### 1. Training Data Enhancements

- **Targeted examples:** Add more examples for low-scoring patterns
- **Language balance:** Ensure balanced training across all languages
- **Edge case coverage:** Add more examples of edge cases

### 2. Algorithm Adjustments

- **Language-specific thresholds:** Consider different thresholds by language
- **Intent refinement:** Clarify boundaries between similar intents
- **Parameter handling:** Improve handling of parameters in commands

### 3. User Experience Improvements

- **Clarification strategies:** Develop better clarification prompts for low confidence
- **Feedback mechanisms:** Implement user feedback for incorrect recognitions
- **Alternative suggestions:** Offer alternatives when confidence is moderate

## Testing Schedule

1. **Day 1:** Baseline testing across all languages
2. **Day 2:** Variation testing
3. **Day 3:** Cross-language comparison
4. **Day 4:** Edge case testing
5. **Day 5:** Analysis and recommendations

## Reporting Format

### Summary Statistics

| Metric | English | Hindi | Hinglish | Overall |
|--------|---------|-------|----------|--------|
| Average Confidence Score | | | | |
| Standard Deviation | | | | |
| % Above 0.75 (High Confidence) | | | | |
| % Below 0.50 (Low Confidence) | | | | |

### Intent-Specific Analysis

| Intent | Avg. English Score | Avg. Hindi Score | Avg. Hinglish Score | Score Variance | Notes |
|--------|-------------------|-----------------|-------------------|---------------|-------|
| GetInventory | | | | | |
| GetOrders | | | | | |
| GetReport | | | | | |

### Key Findings

1. **Strengths:**
   - [List areas where confidence scores are consistently high]

2. **Weaknesses:**
   - [List areas where confidence scores are consistently low]

3. **Inconsistencies:**
   - [List areas with high variance in confidence scores]

4. **Language-Specific Issues:**
   - [List issues specific to each language]

### Recommendations

1. **High Priority:**
   - [List critical improvements needed]

2. **Medium Priority:**
   - [List important but non-critical improvements]

3. **Low Priority:**
   - [List nice-to-have improvements]

## Conclusion

Systematic analysis of confidence scores across languages and command types provides valuable insights for improving the chatbot's intent recognition capabilities. By identifying patterns and addressing issues, you can enhance the accuracy and reliability of the chatbot across all supported languages.

---

*This document should be used alongside the Multilingual WhatsApp Command Testing Plan and Test Case Matrix.*