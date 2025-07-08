# Test Results Recording Template

## Overview

This document provides a standardized template for recording the results of multilingual WhatsApp chatbot testing. The template is designed to be implemented in Excel or Google Sheets for easy tracking, filtering, and analysis of test results.

## Template Structure

### Sheet 1: Test Results Summary

| Column Name | Description | Example Values |
|-------------|-------------|----------------|
| Test ID | Unique identifier for the test case | INV-EN-01, ORD-HI-03, REP-HG-02 |
| Date | Date of test execution | 2023-05-15 |
| Tester | Name of the tester | Ritu Sharma |
| Category | Command category | Inventory, Order, Reporting, Customer |
| Language | Input language | English, Hindi, Hinglish |
| Command | Exact command text | "Show my inventory" |
| Detected Language | Language detected by system | English, Hindi, Hinglish |
| Expected Intent | Expected intent | get_inventory, get_orders, etc. |
| Actual Intent | Intent detected by system | get_inventory, get_orders, etc. |
| Confidence Score | Confidence percentage | 95%, 78%, 65% |
| Status | Test result | Pass, Fail, Warning |
| Issue Types | Types of issues found | Language Detection, Intent Mismatch, etc. |
| Notes | Additional observations | "Response missing product prices" |

### Sheet 2: Detailed Test Records

| Column Name | Description | Example Values |
|-------------|-------------|----------------|
| Test ID | Unique identifier for the test case | INV-EN-01 |
| Command | Exact command text | "Show my inventory" |
| Expected Language | Expected language | English |
| Detected Language | Language detected by system | English |
| Language Detection Correct | Whether language detection was correct | Yes, No |
| Expected Intent | Expected intent | get_inventory |
| Actual Intent | Intent detected by system | get_inventory |
| Intent Recognition Correct | Whether intent recognition was correct | Yes, No |
| Confidence Score | Confidence percentage | 95% |
| Confidence Threshold | Whether confidence is above threshold (70%) | Above, Below |
| Expected Response Pattern | Expected response pattern | List of inventory items with quantities |
| Actual Response | Exact response text | "Here is your current inventory:\n- Product A: 50 units" |
| Response Quality Score | Overall quality score (1-5) | 4.5 |
| Grammatical Accuracy (1-5) | Grammar score | 5 |
| Vocabulary Appropriateness (1-5) | Vocabulary score | 4 |
| Cultural Appropriateness (1-5) | Cultural appropriateness score | 5 |
| Clarity (1-5) | Clarity score | 5 |
| Consistency (1-5) | Consistency score | 4 |
| Natural Language Flow (1-5) | Natural language flow score | 4 |
| Tone (1-5) | Tone score | 5 |
| Status | Test result | Pass, Fail, Warning |
| Issue Types | Types of issues found | Language Detection, Intent Mismatch, etc. |
| Issue Description | Detailed description of issues | "System detected Hinglish as English" |
| Screenshot Reference | Reference to screenshot file | "INV-EN-01.png" |
| Notes | Additional observations | "Response is clear but missing product prices" |

### Sheet 3: Issue Tracking

| Column Name | Description | Example Values |
|-------------|-------------|----------------|
| Issue ID | Unique identifier for the issue | LANG-001, INTENT-003 |
| Related Test IDs | Test cases where issue was found | INV-EN-01, INV-EN-02 |
| Issue Category | Category of the issue | Language Detection, Intent Recognition, Response Quality |
| Issue Type | Specific type of issue | Wrong Language, Mismatch Intent, Grammar Error |
| Issue Description | Detailed description | "System consistently detects Hinglish as English" |
| Severity | Issue severity | Critical, High, Medium, Low |
| Frequency | How often the issue occurs | Always, Often, Sometimes, Rarely |
| Pattern | Pattern of occurrence | "Only with informal commands", "With mixed language" |
| Affected Languages | Languages affected by the issue | English, Hindi, Hinglish |
| Affected Command Types | Command types affected | Inventory, Order, Reporting, Customer |
| Reproducible | Whether issue is consistently reproducible | Yes, No, Sometimes |
| Steps to Reproduce | Steps to reproduce the issue | "1. Enter Hinglish command with English words" |
| Screenshots | References to screenshot files | "LANG-001-1.png, LANG-001-2.png" |
| Status | Current status of the issue | Open, In Progress, Resolved, Verified |
| Assigned To | Person assigned to fix | Abhishek, Rahul |
| Notes | Additional information | "May be related to transliteration issues" |

### Sheet 4: Language Detection Analysis

| Column Name | Description | Example Values |
|-------------|-------------|----------------|
| Language | Input language | English, Hindi, Hinglish |
| Total Tests | Total number of tests | 50, 45, 48 |
| Correct Detection | Number of correct detections | 48, 40, 35 |
| Incorrect Detection | Number of incorrect detections | 2, 5, 13 |
| Detection Accuracy | Percentage of correct detections | 96%, 89%, 73% |
| Common Misdetections | Common incorrect detections | "Hinglish as English", "Mixed as Hindi" |
| Notes | Additional observations | "Hinglish detection needs improvement" |

### Sheet 5: Intent Recognition Analysis

| Column Name | Description | Example Values |
|-------------|-------------|----------------|
| Intent | Intent type | get_inventory, get_orders, etc. |
| Total Tests | Total number of tests | 30, 25, 20 |
| Correct Recognition | Number of correct recognitions | 28, 22, 15 |
| Incorrect Recognition | Number of incorrect recognitions | 2, 3, 5 |
| Recognition Accuracy | Percentage of correct recognitions | 93%, 88%, 75% |
| Average Confidence (Correct) | Average confidence for correct recognitions | 92%, 85%, 80% |
| Average Confidence (Incorrect) | Average confidence for incorrect recognitions | 68%, 62%, 55% |
| Common Misrecognitions | Common incorrect recognitions | "get_custom_report as get_report" |
| Notes | Additional observations | "Informal commands have lower confidence" |

### Sheet 6: Response Quality Analysis

| Column Name | Description | Example Values |
|-------------|-------------|----------------|
| Language | Response language | English, Hindi, Hinglish |
| Total Responses | Total number of responses | 50, 45, 48 |
| Average Quality Score | Average overall quality score | 4.5, 3.8, 4.0 |
| Average Grammar Score | Average grammar score | 4.8, 3.5, 4.2 |
| Average Vocabulary Score | Average vocabulary score | 4.6, 4.0, 4.1 |
| Average Cultural Score | Average cultural appropriateness score | 4.9, 4.5, 4.7 |
| Average Clarity Score | Average clarity score | 4.7, 3.7, 4.0 |
| Average Consistency Score | Average consistency score | 4.4, 3.9, 4.0 |
| Average Flow Score | Average natural language flow score | 4.3, 3.6, 3.8 |
| Average Tone Score | Average tone score | 4.5, 4.2, 4.3 |
| Common Issues | Common quality issues | "Grammar errors in Hindi responses" |
| Notes | Additional observations | "Hindi responses need improvement" |

## Color Coding Guidelines

Use the following color coding scheme for the Status column:

- **Green (#C6EFCE):** Pass - Test passed with no issues
- **Yellow (#FFEB9C):** Warning - Test passed but with minor issues or low confidence
- **Red (#FFC7CE):** Fail - Test failed with significant issues

## Filtering and Analysis Tips

1. **Filter by Status:**
   - Filter for "Fail" status to identify critical issues
   - Filter for "Warning" status to identify areas for improvement

2. **Filter by Language:**
   - Compare performance across languages
   - Identify language-specific issues

3. **Filter by Command Category:**
   - Analyze performance by command type
   - Identify problematic command categories

4. **Filter by Issue Type:**
   - Group similar issues together
   - Identify patterns in issue occurrence

5. **Pivot Tables:**
   - Create pivot tables to analyze pass/fail rates by language
   - Create pivot tables to analyze confidence scores by intent type
   - Create pivot tables to analyze response quality by language

## Data Visualization Suggestions

1. **Bar Charts:**
   - Pass/fail rates by language
   - Pass/fail rates by command category
   - Average confidence scores by language
   - Average quality scores by language

2. **Pie Charts:**
   - Distribution of issue types
   - Distribution of test statuses

3. **Line Charts:**
   - Confidence scores across test cases
   - Quality scores across test cases

4. **Radar Charts:**
   - Quality dimensions by language
   - Performance across different metrics

## Implementation Instructions

1. **Create a Google Sheet or Excel file** with the sheets and columns described above
2. **Set up data validation** for columns with predefined values
3. **Set up conditional formatting** for the Status column using the color coding guidelines
4. **Create formulas** to calculate derived values (e.g., detection accuracy percentages)
5. **Set up pivot tables and charts** for analysis
6. **Share the sheet** with the testing team and stakeholders

## Example Usage

1. **During Testing:**
   - Fill in the Test Results Summary sheet as you conduct each test
   - Add detailed information to the Detailed Test Records sheet
   - Note any issues in the Issue Tracking sheet

2. **After Testing:**
   - Complete the analysis sheets with aggregated data
   - Create visualizations of key metrics
   - Prepare a summary of findings

## Conclusion

This standardized test results recording template provides a comprehensive framework for documenting and analyzing the results of multilingual WhatsApp chatbot testing. By using this template, testers can efficiently track test results, identify patterns in issues, and generate insights to improve the chatbot's performance across English, Hindi, and Hinglish.

---

*This template should be implemented in Excel or Google Sheets and used in conjunction with the comprehensive test execution plan and practical testing guide.*