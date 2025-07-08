# Inventory Report Test Plan

## Overview
This test plan covers the manual testing of the inventory report functionality in OneTappe, focusing on both the WhatsApp chatbot interface and the seller dashboard. The plan ensures that inventory reports are generated correctly, display accurate data, and are accessible across different devices and languages.

## Test Environment
- **Devices**: Mobile (Android/iOS), Desktop (Windows/Mac), Tablet
- **Browsers**: Chrome, Safari, Firefox, Edge
- **Languages**: English, Hindi, Hinglish
- **Test Users**: Seller accounts with varying inventory sizes

## Test Cases

### 1. WhatsApp Chatbot Interface

#### 1.1 Command Recognition

| Test ID | Test Description | Test Steps | Expected Result | Status |
|---------|-----------------|-----------|----------------|--------|
| WA-IR-001 | English command recognition | 1. Send "inventory report" to chatbot<br>2. Send "generate inventory report" | Bot recognizes the intent and responds with success message | ⬜ |
| WA-IR-002 | Hindi command recognition | 1. Send "इन्वेंटरी रिपोर्ट" to chatbot<br>2. Send "इन्वेंटरी रिपोर्ट जनरेट करें" | Bot recognizes the intent and responds with success message in Hindi | ⬜ |
| WA-IR-003 | Hinglish command recognition | 1. Send "inventory report banao" to chatbot<br>2. Send "mera inventory report chahiye" | Bot recognizes the intent and responds appropriately | ⬜ |

#### 1.2 Response Format

| Test ID | Test Description | Test Steps | Expected Result | Status |
|---------|-----------------|-----------|----------------|--------|
| WA-IR-004 | Success message format (English) | Send "inventory report" to chatbot | Response includes confirmation and instructions to access the report | ⬜ |
| WA-IR-005 | Success message format (Hindi) | Send "इन्वेंटरी रिपोर्ट" to chatbot | Response includes confirmation and instructions in Hindi | ⬜ |
| WA-IR-006 | Link to dashboard in response | Send inventory report command | Response includes a direct link to access the report in the dashboard | ⬜ |

#### 1.3 Error Handling

| Test ID | Test Description | Test Steps | Expected Result | Status |
|---------|-----------------|-----------|----------------|--------|
| WA-IR-007 | Empty inventory | Send inventory report command from seller with no products | Appropriate message indicating empty inventory | ⬜ |
| WA-IR-008 | Server error | Simulate server error during report generation | Error message with retry instructions | ⬜ |
| WA-IR-009 | Authentication failure | Send command with expired session | Authentication error with login instructions | ⬜ |

### 2. PDF Report Generation

#### 2.1 Report Content

| Test ID | Test Description | Test Steps | Expected Result | Status |
|---------|-----------------|-----------|----------------|--------|
| PDF-IR-001 | Header information | Generate report and check header | Contains seller name, business name, date and time | ⬜ |
| PDF-IR-002 | Summary statistics | Check summary section of report | Shows total products, total stock, low stock count, out of stock count | ⬜ |
| PDF-IR-003 | Product details | Check product table in report | Each product shows ID, name, category, price, stock, status | ⬜ |
| PDF-IR-004 | Status indicators | Check status column for products | Low stock items highlighted in yellow, out of stock in red | ⬜ |
| PDF-IR-005 | Large inventory handling | Generate report for seller with 100+ products | Report correctly paginates and shows all products | ⬜ |

#### 2.2 PDF Format and Accessibility

| Test ID | Test Description | Test Steps | Expected Result | Status |
|---------|-----------------|-----------|----------------|--------|
| PDF-IR-006 | File format | Check downloaded file | Valid PDF that opens in standard PDF viewers | ⬜ |
| PDF-IR-007 | File naming | Check filename of downloaded report | Contains seller ID and date in format "inventory_report_[sellerID]_[YYYYMMDD].pdf" | ⬜ |
| PDF-IR-008 | File size | Generate and check file size | Reasonable size (<2MB for typical inventory) | ⬜ |
| PDF-IR-009 | Mobile viewing | Open PDF on mobile device | Content is readable on small screens | ⬜ |

### 3. Dashboard Integration

#### 3.1 Report Access

| Test ID | Test Description | Test Steps | Expected Result | Status |
|---------|-----------------|-----------|----------------|--------|
| DASH-IR-001 | Report button visibility | Login to seller dashboard | "Inventory Report" button is visible in reports section | ⬜ |
| DASH-IR-002 | Report generation flow | Click "Generate Inventory Report" button | Loading indicator shown, then download starts | ⬜ |
| DASH-IR-003 | Report history | Check reports section | Previously generated reports are listed with dates | ⬜ |

#### 3.2 Cross-Device Compatibility

| Test ID | Test Description | Test Steps | Expected Result | Status |
|---------|-----------------|-----------|----------------|--------|
| DASH-IR-004 | Desktop browsers | Generate report on Chrome, Firefox, Safari, Edge | Report generates and downloads correctly on all browsers | ⬜ |
| DASH-IR-005 | Mobile browsers | Generate report on mobile Chrome and Safari | Report generates and can be viewed on mobile | ⬜ |
| DASH-IR-006 | Tablet view | Access dashboard on tablet | Report button is accessible and functional | ⬜ |

#### 3.3 Language Support

| Test ID | Test Description | Test Steps | Expected Result | Status |
|---------|-----------------|-----------|----------------|--------|
| DASH-IR-007 | English interface | Set dashboard language to English | Report button and flow in English | ⬜ |
| DASH-IR-008 | Hindi interface | Set dashboard language to Hindi | Report button and flow in Hindi | ⬜ |
| DASH-IR-009 | PDF language match | Generate report with Hindi interface | PDF headers and labels in Hindi | ⬜ |

## Test Execution Checklist

### Pre-requisites
- [ ] Test seller accounts created with varying inventory sizes
- [ ] Test environments set up on different devices and browsers
- [ ] Test data prepared (products with normal, low, and zero stock)

### Test Execution
- [ ] Execute all WhatsApp interface tests
- [ ] Execute all PDF report content tests
- [ ] Execute all dashboard integration tests
- [ ] Document any bugs or issues found

### Post-Test Activities
- [ ] Compile test results
- [ ] Create bug reports for any issues
- [ ] Verify fixed issues in subsequent test cycles
- [ ] Update test plan based on findings

## Bug Reporting Template

**Bug ID**: [Auto-generated]

**Test Case ID**: [Related test case]

**Summary**: [Brief description of the issue]

**Steps to Reproduce**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result**: [What should happen]

**Actual Result**: [What actually happened]

**Environment**:
- Device: [Device model]
- OS: [Operating system and version]
- Browser: [Browser and version]
- Language: [Interface language]

**Severity**: [Critical/High/Medium/Low]

**Priority**: [High/Medium/Low]

**Screenshots/Videos**: [Attach if available]

**Notes**: [Any additional information]