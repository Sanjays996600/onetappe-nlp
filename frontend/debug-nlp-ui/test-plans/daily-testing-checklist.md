# Daily Testing Checklist for WhatsApp Chatbot Language QA

This checklist provides a structured approach for daily testing of the WhatsApp chatbot's language capabilities. It is designed to be used alongside the comprehensive test case matrix and other testing documents.

## Pre-Testing Setup

- [ ] Open the debug UI at http://localhost:3000
- [ ] Prepare your testing spreadsheet or document for recording results
- [ ] Review any recent changes or updates to the chatbot
- [ ] Check that the test environment is functioning correctly
- [ ] Clear any previous test data or conversations if necessary

## Daily Testing Schedule

### Day 1: Inventory Management Commands

#### Morning Session (English)
- [ ] Test "Get Inventory" commands (INV-ENG-01 to INV-ENG-05)
- [ ] Test "Get Low Stock" commands (INV-ENG-06 to INV-ENG-10)
- [ ] Test "Edit Stock" commands (INV-ENG-11 to INV-ENG-15)
- [ ] Test "Add Product" commands (INV-ENG-16 to INV-ENG-20)

#### Afternoon Session (Hindi & Hinglish)
- [ ] Test "Get Inventory" commands in Hindi (INV-HIN-01 to INV-HIN-05)
- [ ] Test "Get Inventory" commands in Hinglish (INV-HGL-01 to INV-HGL-05)
- [ ] Test "Get Low Stock" commands in Hindi (INV-HIN-06 to INV-HIN-10)
- [ ] Test "Get Low Stock" commands in Hinglish (INV-HGL-06 to INV-HGL-10)
- [ ] Test "Edit Stock" commands in Hindi (INV-HIN-11 to INV-HIN-15)
- [ ] Test "Edit Stock" commands in Hinglish (INV-HGL-11 to INV-HGL-15)
- [ ] Test "Add Product" commands in Hindi (INV-HIN-16 to INV-HIN-20)
- [ ] Test "Add Product" commands in Hinglish (INV-HGL-16 to INV-HGL-20)

### Day 2: Order Management Commands

#### Morning Session (English)
- [ ] Test "Get Orders" commands (ORD-ENG-01 to ORD-ENG-05)
- [ ] Test "Get Order Details" commands (ORD-ENG-06 to ORD-ENG-10)
- [ ] Test "Update Order Status" commands (ORD-ENG-11 to ORD-ENG-15)

#### Afternoon Session (Hindi & Hinglish)
- [ ] Test "Get Orders" commands in Hindi (ORD-HIN-01 to ORD-HIN-05)
- [ ] Test "Get Orders" commands in Hinglish (ORD-HGL-01 to ORD-HGL-05)
- [ ] Test "Get Order Details" commands in Hindi (ORD-HIN-06 to ORD-HIN-10)
- [ ] Test "Get Order Details" commands in Hinglish (ORD-HGL-06 to ORD-HGL-10)
- [ ] Test "Update Order Status" commands in Hindi (ORD-HIN-11 to ORD-HIN-15)
- [ ] Test "Update Order Status" commands in Hinglish (ORD-HGL-11 to ORD-HGL-15)

### Day 3: Reporting Commands

#### Morning Session (English)
- [ ] Test "Get Report" commands (REP-ENG-01 to REP-ENG-05)
- [ ] Test "Get Custom Report" commands (REP-ENG-06 to REP-ENG-10)

#### Afternoon Session (Hindi & Hinglish)
- [ ] Test "Get Report" commands in Hindi (REP-HIN-01 to REP-HIN-05)
- [ ] Test "Get Report" commands in Hinglish (REP-HGL-01 to REP-HGL-05)
- [ ] Test "Get Custom Report" commands in Hindi (REP-HIN-06 to REP-HIN-10)
- [ ] Test "Get Custom Report" commands in Hinglish (REP-HGL-06 to REP-HGL-10)

### Day 4: Customer Data Commands

#### Morning Session (English)
- [ ] Test "Get Customer Data" commands (CUS-ENG-01 to CUS-ENG-05)

#### Afternoon Session (Hindi & Hinglish)
- [ ] Test "Get Customer Data" commands in Hindi (CUS-HIN-01 to CUS-HIN-05)
- [ ] Test "Get Customer Data" commands in Hinglish (CUS-HGL-01 to CUS-HGL-05)

### Day 5: Edge Cases

#### Morning Session
- [ ] Test "Typos and Misspellings" in all languages (EDG-ENG-01 to EDG-HGL-03)
- [ ] Test "Abbreviated Text" cases (EDG-HGL-04 to EDG-HGL-06)
- [ ] Test "Mixed Language" cases (EDG-MIX-01 to EDG-MIX-09)

#### Afternoon Session
- [ ] Test "Commands with Emojis" in all languages (EDG-EMJ-01 to EDG-EMJ-09)
- [ ] Test "Ambiguous Requests" in all languages (EDG-AMB-01 to EDG-AMB-09)
- [ ] Test "Multiple Intents" in all languages (EDG-MLT-01 to EDG-MLT-06)

## Testing Procedure for Each Command

1. [ ] Enter the command exactly as specified in the test case
2. [ ] Note the detected language
3. [ ] Note the predicted intent
4. [ ] Note the confidence score
5. [ ] Note the response
6. [ ] Evaluate if the test passed or failed
7. [ ] If failed, classify the issue using appropriate tags
8. [ ] Add any additional observations or notes
9. [ ] Take screenshots of notable issues

## Issue Classification Checklist

### Intent Recognition Issues
- [ ] Wrong intent detected
- [ ] No intent detected
- [ ] Low confidence score (below threshold)

### Language Detection Issues
- [ ] Wrong language detected
- [ ] Mixed language not properly handled

### Response Quality Issues
- [ ] Grammatical errors
- [ ] Unnatural phrasing
- [ ] Incorrect information
- [ ] Missing information
- [ ] Tone issues (not friendly/helpful)

### Edge Case Issues
- [ ] Typo handling problems
- [ ] Abbreviation handling problems
- [ ] Mixed language handling problems
- [ ] Emoji handling problems
- [ ] Multiple intent handling problems

## Daily Summary

- [ ] Compile a summary of tests completed
- [ ] Highlight key issues discovered
- [ ] Identify patterns in failures
- [ ] Prioritize issues for resolution
- [ ] Share findings with development team

## Weekly Review

- [ ] Review all test results from the week
- [ ] Identify trends and patterns
- [ ] Compare performance across languages
- [ ] Prepare summary report
- [ ] Discuss findings in team meeting

## Notes

- Focus on one command type at a time to maintain consistency
- Take short breaks between testing sessions to maintain focus
- If you find a critical issue, report it immediately rather than waiting for the daily summary
- Keep track of any improvements or regressions compared to previous testing cycles
- Document any new edge cases or command variations you discover during testing

---

*This checklist should be used alongside the comprehensive test case matrix and other testing documents.*