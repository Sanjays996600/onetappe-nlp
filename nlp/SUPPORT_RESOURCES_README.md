# One Tappe Support Resources

This directory contains resources for the Support Executive team to assist beta sellers using the One Tappe platform.

## Files Overview

### 1. WhatsApp Support Snippets (`whatsapp_support_snippets.json`)

A comprehensive collection of message templates in both English and Hindi for various support scenarios:

- **Welcome & Onboarding**: Initial greetings and command introductions
- **Inventory Commands**: Templates for inventory viewing, product addition, stock updates, etc.
- **Sales Report Queries**: Templates for various report requests
- **Order Help**: Templates for order-related assistance
- **Low Stock Alerts**: Notifications and threshold explanations
- **Error Responses**: Common error messages and troubleshooting
- **Help & Escalation**: General help and escalation procedures

#### Usage:

```python
import json

# Load the snippets
with open('whatsapp_support_snippets.json', 'r', encoding='utf-8') as f:
    snippets = json.load(f)

# Example: Get welcome message in English
welcome_en = snippets['welcome_onboarding']['initial_greeting']['en']

# Example: Get inventory help in Hindi
inventory_help_hi = snippets['inventory_commands']['view_inventory']['hi']
```

### 2. Seller Support Tracker Template (`seller_support_tracker_template.csv`)

A CSV template for tracking support tickets and WhatsApp-based seller issues with the following fields:

- WhatsApp Number
- Seller Name
- Issue Type (Bug / Help / Feature Request / Complaint)
- Description
- Status (Pending, Resolved, Escalated)
- Assigned To
- Resolution Summary
- Timestamp

#### Usage:

1. Import this CSV into Google Sheets or Excel
2. Share with the QA, Tech, and Operations teams
3. Update regularly as new issues come in and are resolved

### 3. WhatsApp Onboarding Broadcast Templates (`whatsapp_onboarding_broadcast_templates.json`)

Three short messages for inviting sellers to the beta program:

- **Initial Invitation**: Introduction to One Tappe
- **Feature Highlight**: Key benefits and features
- **Action Required**: Call-to-action with instructions

Each template is available in both English and Hindi.

#### Usage:

```python
import json

# Load the broadcast templates
with open('whatsapp_onboarding_broadcast_templates.json', 'r', encoding='utf-8') as f:
    broadcasts = json.load(f)

# Example: Get initial invitation in English
initial_invitation_en = broadcasts['onboarding_broadcasts']['initial_invitation']['en']

# Example: Get action required message in Hindi
action_required_hi = broadcasts['onboarding_broadcasts']['action_required']['hi']
```

## Best Practices for Support Executives

1. **Be Proactive**: Reach out to sellers who haven't been active for a few days
2. **Document Everything**: Keep the support tracker updated with all interactions
3. **Use Templates Wisely**: Customize templates to make them personal, don't just copy-paste
4. **Follow Up**: Check back with sellers after resolving issues to ensure satisfaction
5. **Escalate Properly**: Use the proper channels for bugs and technical issues
6. **Collect Feedback**: Note suggestions and pain points for product improvement

## Escalation Process

1. **Level 1**: Support Executive (You) - First response within 30 minutes
2. **Level 2**: Technical Support - For bugs and technical issues (escalate via Slack)
3. **Level 3**: Product Team - For feature requests and major issues (escalate via ClickUp)

## Language Guidelines

- Always respond in the same language the seller used to contact you
- For mixed language messages, follow the predominant language
- Keep messages concise and easy to understand
- Use emojis to make messages friendly but don't overdo it

---

For any questions about these resources, please contact the Support Team Lead.