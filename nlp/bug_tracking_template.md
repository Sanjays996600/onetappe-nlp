# NLP Command System Bug Tracking Template

## Overview
This template provides a standardized format for documenting and tracking bugs found during testing of the NLP command system. Using a consistent format helps ensure that all necessary information is captured for efficient debugging and resolution.

## Bug Report Template

```markdown
# Bug Report: [BUG-ID]

## Basic Information
- **Bug ID**: [Unique identifier, e.g., BUG-001]
- **Reporter**: [Name of the person reporting the bug]
- **Date Reported**: [YYYY-MM-DD]
- **Priority**: [Critical/High/Medium/Low]
- **Severity**: [Blocker/Major/Minor/Cosmetic]
- **Status**: [New/In Progress/Fixed/Verified/Closed]
- **Assigned To**: [Name of person assigned to fix the bug]
- **Component**: [Intent Recognition/Entity Extraction/Command Routing/WhatsApp Integration/API Integration/Other]
- **Language**: [English/Hindi/Both/N/A]

## Description
[Clear, concise description of the bug]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]
...

## Expected Behavior
[What should happen when the steps are followed]

## Actual Behavior
[What actually happens when the steps are followed]

## Test Environment
- **OS**: [Operating system and version]
- **Python Version**: [Python version]
- **Dependencies**: [Relevant package versions]
- **Test Data**: [Link to test data if applicable]

## Screenshots/Logs
[Include relevant screenshots, log outputs, or error messages]

## Possible Cause
[If known, describe the potential cause of the bug]

## Suggested Fix
[If known, suggest a possible solution]

## Related Issues
[Link to related bugs or issues]

## Notes
[Any additional information that might be helpful]

## Resolution
- **Fixed By**: [Name of person who fixed the bug]
- **Fix Date**: [YYYY-MM-DD]
- **Fix Version**: [Version where the fix was implemented]
- **Resolution Details**: [Description of how the bug was fixed]
- **Verification**: [How the fix was verified]
```

## Priority Levels

- **Critical**: Bug prevents core functionality from working, blocks testing, or could cause data loss/security issues.
- **High**: Bug significantly impacts functionality but has workarounds, affects many users.
- **Medium**: Bug has moderate impact on functionality, affects some users, has easy workarounds.
- **Low**: Bug has minimal impact, affects few users, is cosmetic, or has trivial consequences.

## Severity Levels

- **Blocker**: System/component is unusable, no workaround exists.
- **Major**: Major functionality is impacted, workaround exists but is cumbersome.
- **Minor**: Minor functionality is impacted, easy workaround exists.
- **Cosmetic**: Visual or text issue that doesn't affect functionality.

## Status Definitions

- **New**: Bug has been reported but not yet reviewed.
- **Confirmed**: Bug has been reviewed and confirmed.
- **In Progress**: Bug is currently being addressed.
- **Fixed**: Bug has been fixed but not yet verified.
- **Verified**: Fix has been verified in testing.
- **Closed**: Bug has been resolved and verified in production.
- **Rejected**: Not considered a bug or won't be fixed.
- **Duplicate**: Already reported in another bug report.

## Example Bug Report

```markdown
# Bug Report: BUG-023

## Basic Information
- **Bug ID**: BUG-023
- **Reporter**: Priya Sharma
- **Date Reported**: 2023-06-15
- **Priority**: High
- **Severity**: Major
- **Status**: Fixed
- **Assigned To**: Rahul Verma
- **Component**: Entity Extraction
- **Language**: Hindi

## Description
The system fails to correctly extract numeric limits from Hindi commands when the number is written in Hindi numerals (e.g., "१०" instead of "10").

## Steps to Reproduce
1. Send the command "टॉप १० प्रोडक्ट्स दिखाओ" (Show top 10 products)
2. Observe the extracted entities in the system logs

## Expected Behavior
The system should extract the limit entity with a value of 10.

## Actual Behavior
The system fails to extract any limit entity and defaults to 5.

## Test Environment
- **OS**: Ubuntu 20.04
- **Python Version**: 3.9.5
- **Dependencies**: spaCy 3.4.0, custom NER model v2.1
- **Test Data**: hindi_commands_test_set.csv, row 23

## Screenshots/Logs
```
INFO:nlp.multilingual_handler:Processing command: टॉप १० प्रोडक्ट्स दिखाओ
INFO:nlp.multilingual_handler:Detected language: hi
INFO:nlp.multilingual_handler:Detected intent: get_top_products
INFO:nlp.multilingual_handler:Extracted entities: {}
INFO:nlp.command_router:Using default limit: 5
```

## Possible Cause
The entity extraction regex pattern only looks for Arabic numerals (0-9) and doesn't account for Hindi numerals (०-९).

## Suggested Fix
Update the regex pattern in `hindi_entity_extractor.py` to include Hindi numerals and convert them to integers.

## Related Issues
BUG-019: Similar issue with Bengali numerals

## Notes
This affects approximately 15% of Hindi users based on usage analytics.

## Resolution
- **Fixed By**: Rahul Verma
- **Fix Date**: 2023-06-18
- **Fix Version**: v2.3.0
- **Resolution Details**: Added support for Hindi numerals in the regex pattern and implemented a conversion function to map Hindi numerals to Arabic numerals before parsing as integers.
- **Verification**: Tested with 20 different commands using Hindi numerals, all correctly extracted the numeric values.
```

## Bug Tracking Workflow

1. **Bug Discovery**
   - Tester identifies a bug during testing
   - Bug is documented using the template
   - Bug is assigned a unique ID

2. **Bug Triage**
   - Bug is reviewed by the QA lead
   - Priority and severity are assigned
   - Bug is assigned to a developer

3. **Bug Resolution**
   - Developer investigates and fixes the bug
   - Developer updates the bug report with resolution details
   - Developer changes status to "Fixed"

4. **Bug Verification**
   - QA tests the fix
   - If verified, status is changed to "Verified"
   - If not verified, status is changed back to "In Progress"

5. **Bug Closure**
   - Bug is closed after being verified in production
   - Metrics are updated

## Bug Metrics

Track the following metrics to monitor bug management efficiency:

- **Bug Discovery Rate**: Number of new bugs per week/sprint
- **Bug Resolution Rate**: Number of bugs fixed per week/sprint
- **Average Time to Resolution**: Average time from bug report to fix
- **Bug Density**: Number of bugs per feature/component
- **Regression Rate**: Percentage of bugs that are regressions

## Best Practices

1. **Be Specific**: Provide clear, concise descriptions and steps to reproduce.
2. **Include Context**: Add relevant logs, screenshots, and environment details.
3. **Update Promptly**: Keep the bug status and information up to date.
4. **Link Related Issues**: Connect related bugs to identify patterns.
5. **Prioritize Effectively**: Focus on high-impact bugs first.
6. **Verify Thoroughly**: Ensure fixes are properly tested before closing bugs.
7. **Learn from Patterns**: Analyze bug trends to improve development practices.

## Conclusion

Consistent bug tracking is essential for maintaining software quality. This template provides a standardized approach to documenting and managing bugs in the NLP command system, ensuring that issues are properly captured, addressed, and verified.