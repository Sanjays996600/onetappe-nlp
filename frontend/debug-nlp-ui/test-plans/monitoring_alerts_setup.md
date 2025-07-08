# Monitoring Alerts for NLP Issues

## Overview

This document outlines the monitoring alert setup for the WhatsApp chatbot NLP system, focusing on critical test failures that should trigger alerts on the Grafana monitoring dashboard. The monitoring system is designed to provide early warning of potential issues in the production environment, allowing for quick intervention before they impact users.

## Alert Categories

### 1. Language Detection Alerts

| Alert ID | Description | Threshold | Severity | Action |
|----------|-------------|-----------|----------|--------|
| LD-ALERT-001 | Language detection confidence below threshold | <80% confidence for 3 consecutive requests | High | Notify QA team |
| LD-ALERT-002 | Language detection accuracy drop | <85% accuracy over 1-hour window | Critical | Notify QA and Dev teams |
| LD-ALERT-003 | Language detection latency | >500ms average over 5 minutes | Medium | Notify Dev team |
| LD-ALERT-004 | Language detection service errors | >1% error rate over 5 minutes | Critical | Notify DevOps and Dev teams |

### 2. Intent Recognition Alerts

| Alert ID | Description | Threshold | Severity | Action |
|----------|-------------|-----------|----------|--------|
| IR-ALERT-001 | Intent recognition confidence below threshold | <70% confidence for 3 consecutive requests | High | Notify QA team |
| IR-ALERT-002 | Intent recognition accuracy drop | <80% accuracy over 1-hour window | Critical | Notify QA and Dev teams |
| IR-ALERT-003 | Intent recognition latency | >800ms average over 5 minutes | Medium | Notify Dev team |
| IR-ALERT-004 | Intent recognition service errors | >1% error rate over 5 minutes | Critical | Notify DevOps and Dev teams |
| IR-ALERT-005 | Multiple intent clarifications required | >10% of requests requiring >2 clarifications in 1 hour | High | Notify QA team |

### 3. Response Quality Alerts

| Alert ID | Description | Threshold | Severity | Action |
|----------|-------------|-----------|----------|--------|
| RQ-ALERT-001 | Response quality score drop | <3.5 average score over 1-hour window | High | Notify QA team |
| RQ-ALERT-002 | Response generation errors | >1% error rate over 5 minutes | Critical | Notify DevOps and Dev teams |
| RQ-ALERT-003 | Response latency | >1.5s average over 5 minutes | Medium | Notify Dev team |
| RQ-ALERT-004 | Response format errors | >2% of responses with format errors in 1 hour | High | Notify QA and Dev teams |

### 4. System Performance Alerts

| Alert ID | Description | Threshold | Severity | Action |
|----------|-------------|-----------|----------|--------|
| SYS-ALERT-001 | NLP service high CPU usage | >80% for 5 minutes | High | Notify DevOps team |
| SYS-ALERT-002 | NLP service high memory usage | >80% for 5 minutes | High | Notify DevOps team |
| SYS-ALERT-003 | NLP service instance down | Any instance down for >1 minute | Critical | Notify DevOps and Dev teams |
| SYS-ALERT-004 | Database connection errors | >1% error rate over 1 minute | Critical | Notify DevOps team |
| SYS-ALERT-005 | API rate limiting triggered | Any occurrence | Medium | Notify DevOps team |

## Prometheus Metrics Configuration

### Language Detection Metrics

```yaml
# Language detection confidence histogram
language_detection_confidence_histogram{language="english|hindi|hinglish"}

# Language detection accuracy (calculated from ground truth in test environment)
language_detection_accuracy_gauge{language="english|hindi|hinglish"}

# Language detection latency histogram
language_detection_latency_histogram{language="english|hindi|hinglish"}

# Language detection errors counter
language_detection_errors_total{error_type="service_error|timeout|invalid_input"}
```

### Intent Recognition Metrics

```yaml
# Intent recognition confidence histogram
intent_recognition_confidence_histogram{intent_type="inventory|order|reporting|customer|other"}

# Intent recognition accuracy (calculated from ground truth in test environment)
intent_recognition_accuracy_gauge{intent_type="inventory|order|reporting|customer|other"}

# Intent recognition latency histogram
intent_recognition_latency_histogram{intent_type="inventory|order|reporting|customer|other"}

# Intent recognition errors counter
intent_recognition_errors_total{error_type="service_error|timeout|invalid_input"}

# Intent clarification counter
intent_clarification_required_total{clarification_count="1|2|3+"}
```

### Response Quality Metrics

```yaml
# Response quality score gauge
response_quality_score_gauge{language="english|hindi|hinglish", response_type="inventory|order|reporting|customer|other"}

# Response generation errors counter
response_generation_errors_total{error_type="service_error|timeout|invalid_input"}

# Response latency histogram
response_latency_histogram{language="english|hindi|hinglish", response_type="inventory|order|reporting|customer|other"}

# Response format errors counter
response_format_errors_total{error_type="missing_field|invalid_format|truncated"}
```

### System Performance Metrics

```yaml
# CPU usage gauge
process_cpu_usage{service="nlp_service", instance="$instance"}

# Memory usage gauge
process_memory_usage{service="nlp_service", instance="$instance"}

# Service up gauge (1 = up, 0 = down)
service_up{service="nlp_service", instance="$instance"}

# Database connection errors counter
database_connection_errors_total{database="main|replica"}

# API rate limiting counter
api_rate_limiting_total{endpoint="/detect_language|/recognize_intent|/generate_response"}
```

## Grafana Alert Rules

### Language Detection Alert Rules

```yaml
# LD-ALERT-001: Language detection confidence below threshold
name: LanguageDetectionLowConfidence
expr: |
  min_over_time(
    avg by (language) (
      rate(language_detection_confidence_histogram_sum{language=~"english|hindi|hinglish"}[1m]) /
      rate(language_detection_confidence_histogram_count{language=~"english|hindi|hinglish"}[1m])
    )[3m:1m]
  ) < 0.8
for: 1m
labels:
  severity: high
  team: qa
annotations:
  summary: Language detection confidence below threshold
  description: Language detection confidence has been below 80% for 3 consecutive requests

# LD-ALERT-002: Language detection accuracy drop
expr: |
  avg_over_time(
    language_detection_accuracy_gauge{language=~"english|hindi|hinglish"}[1h]
  ) < 0.85
for: 5m
labels:
  severity: critical
  team: qa,dev
annotations:
  summary: Language detection accuracy drop
  description: Language detection accuracy has been below 85% over the last hour
```

### Intent Recognition Alert Rules

```yaml
# IR-ALERT-001: Intent recognition confidence below threshold
name: IntentRecognitionLowConfidence
expr: |
  min_over_time(
    avg by (intent_type) (
      rate(intent_recognition_confidence_histogram_sum{intent_type=~"inventory|order|reporting|customer|other"}[1m]) /
      rate(intent_recognition_confidence_histogram_count{intent_type=~"inventory|order|reporting|customer|other"}[1m])
    )[3m:1m]
  ) < 0.7
for: 1m
labels:
  severity: high
  team: qa
annotations:
  summary: Intent recognition confidence below threshold
  description: Intent recognition confidence has been below 70% for 3 consecutive requests

# IR-ALERT-005: Multiple intent clarifications required
name: MultipleIntentClarificationsRequired
expr: |
  sum(increase(intent_clarification_required_total{clarification_count=~"2|3+"}[1h])) /
  sum(increase(intent_clarification_required_total{clarification_count=~"1|2|3+"}[1h])) > 0.1
for: 5m
labels:
  severity: high
  team: qa
annotations:
  summary: Multiple intent clarifications required
  description: More than 10% of requests required multiple clarifications in the last hour
```

## Integration with Debug UI

The monitoring system is integrated with the Debug UI to provide real-time visibility into alerts and metrics. This integration enables QA testers and developers to quickly identify and diagnose issues during testing.

### Debug UI Alert Panel

The Debug UI includes an Alert Panel that displays:

1. **Active Alerts**: Currently triggered alerts with severity, description, and duration
2. **Recent Alerts**: Alerts that were triggered in the last 24 hours
3. **Alert Trends**: Charts showing alert frequency over time

### Alert to Debug UI Mapping

When an alert is triggered, the Debug UI provides direct links to relevant sections:

| Alert Type | Debug UI Section | Information Displayed |
|------------|------------------|----------------------|
| Language Detection | Language Analysis | Confidence scores, detected language, ground truth |
| Intent Recognition | Intent Analysis | Confidence scores, detected intent, ground truth |
| Response Quality | Response Evaluation | Quality scores, response text, issues detected |
| System Performance | System Metrics | CPU/memory usage, latency, error rates |

### Alert Investigation Workflow

1. Alert is triggered in Grafana
2. Notification is sent to appropriate team(s)
3. Team member opens Debug UI and navigates to the Alert Panel
4. Clicks on the alert to view details and navigate to relevant Debug UI section
5. Investigates the issue using the Debug UI tools
6. Documents findings and creates issue ticket if needed

## Alert Notification Channels

### Team Notifications

| Team | Primary Channel | Secondary Channel | Escalation Channel |
|------|----------------|-------------------|-------------------|
| QA | Slack (#qa-alerts) | Email | Phone (Critical only) |
| Dev | Slack (#dev-alerts) | Email | Phone (Critical only) |
| DevOps | Slack (#devops-alerts) | PagerDuty | Phone |

### Notification Templates

#### Slack Notification

```
[{{ .Labels.severity | toUpper }}] {{ .AlertName }}

Description: {{ .Annotations.description }}
Value: {{ .Value }}
Threshold: {{ .Annotations.threshold }}
Duration: {{ .For }}

View in Grafana: {{ .DashboardURL }}
View in Debug UI: {{ .ExternalURL }}/debug-ui/alerts?id={{ .AlertName }}
```

#### Email Notification

```
Subject: [{{ .Labels.severity | toUpper }}] WhatsApp Chatbot Alert: {{ .AlertName }}

Alert: {{ .AlertName }}
Severity: {{ .Labels.severity | toUpper }}
Description: {{ .Annotations.description }}

Value: {{ .Value }}
Threshold: {{ .Annotations.threshold }}
Duration: {{ .For }}

View in Grafana: {{ .DashboardURL }}
View in Debug UI: {{ .ExternalURL }}/debug-ui/alerts?id={{ .AlertName }}

This is an automated message. Please do not reply to this email.
```

## Alert Response Procedures

### Critical Alerts

1. Immediate acknowledgment required (within 5 minutes)
2. Begin investigation using Debug UI
3. If not resolved within 15 minutes, escalate to senior team member
4. Document all actions taken in incident log
5. Post-incident review required

### High Alerts

1. Acknowledgment required within 15 minutes
2. Begin investigation using Debug UI
3. If not resolved within 30 minutes, update status and estimate resolution time
4. Document actions in issue tracking system

### Medium Alerts

1. Acknowledgment required within 30 minutes
2. Investigate during business hours
3. Document in issue tracking system

## Grafana Dashboard Setup

### Main NLP Monitoring Dashboard

The main NLP monitoring dashboard includes the following panels:

1. **Language Detection Overview**
   - Confidence scores by language
   - Accuracy trends
   - Error rates
   - Latency metrics

2. **Intent Recognition Overview**
   - Confidence scores by intent type
   - Accuracy trends
   - Error rates
   - Clarification frequency
   - Latency metrics

3. **Response Quality Overview**
   - Quality scores by language and response type
   - Error rates
   - Latency metrics

4. **System Performance Overview**
   - CPU and memory usage
   - Service availability
   - Database connection status
   - API rate limiting status

5. **Alert History**
   - Recent alerts with resolution status
   - Alert frequency by type
   - Mean time to resolution

### Dashboard JSON Example

```json
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "id": 1,
  "links": [],
  "panels": [
    {
      "alert": {
        "alertRuleTags": {},
        "conditions": [
          {
            "evaluator": {
              "params": [
                0.8
              ],
              "type": "lt"
            },
            "operator": {
              "type": "and"
            },
            "query": {
              "params": [
                "A",
                "5m",
                "now"
              ]
            },
            "reducer": {
              "params": [],
              "type": "min"
            },
            "type": "query"
          }
        ],
        "executionErrorState": "alerting",
        "for": "5m",
        "frequency": "1m",
        "handler": 1,
        "name": "Language Detection Confidence Alert",
        "noDataState": "no_data",
        "notifications": []
      },
      "aliasColors": {},
      "bars": false,
      "dashLength": 10,
      "dashes": false,
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "fill": 1,
      "fillGradient": 0,
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 0
      },
      "hiddenSeries": false,
      "id": 2,
      "legend": {
        "avg": false,
        "current": false,
        "max": false,
        "min": false,
        "show": true,
        "total": false,
        "values": false
      },
      "lines": true,
      "linewidth": 1,
      "nullPointMode": "null",
      "options": {
        "alertThreshold": true
      },
      "percentage": false,
      "pluginVersion": "7.3.7",
      "pointradius": 2,
      "points": false,
      "renderer": "flot",
      "seriesOverrides": [],
      "spaceLength": 10,
      "stack": false,
      "steppedLine": false,
      "targets": [
        {
          "expr": "avg by (language) (\n  rate(language_detection_confidence_histogram_sum{language=~\"english|hindi|hinglish\"}[1m]) /\n  rate(language_detection_confidence_histogram_count{language=~\"english|hindi|hinglish\"}[1m])\n)",
          "interval": "",
          "legendFormat": "{{language}}",
          "refId": "A"
        }
      ],
      "thresholds": [
        {
          "colorMode": "critical",
          "fill": true,
          "line": true,
          "op": "lt",
          "value": 0.8
        }
      ],
      "timeFrom": null,
      "timeRegions": [],
      "timeShift": null,
      "title": "Language Detection Confidence",
      "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
      },
      "type": "graph",
      "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": []
      },
      "yaxes": [
        {
          "format": "percentunit",
          "label": null,
          "logBase": 1,
          "max": "1",
          "min": "0",
          "show": true
        },
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        }
      ],
      "yaxis": {
        "align": false,
        "alignLevel": null
      }
    }
  ],
  "schemaVersion": 26,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "NLP Monitoring Dashboard",
  "uid": "nlp-monitoring",
  "version": 1
}
```

## Implementation Steps

### 1. Instrument NLP Services

1. Add Prometheus client libraries to NLP services
2. Define and implement metrics collection for all required metrics
3. Expose metrics endpoints for Prometheus scraping
4. Validate metrics collection with test queries

### 2. Configure Prometheus

1. Update Prometheus configuration to scrape NLP service metrics
2. Define recording rules for complex metrics calculations
3. Set up alerting rules based on the defined thresholds
4. Test alert triggering with synthetic data

### 3. Set Up Grafana Dashboards

1. Create main NLP monitoring dashboard
2. Configure alert notifications
3. Set up user permissions for different teams
4. Test dashboard functionality and alert notifications

### 4. Integrate with Debug UI

1. Implement Alert Panel in Debug UI
2. Create API endpoints for retrieving alert data
3. Add direct links from alerts to relevant Debug UI sections
4. Test integration with simulated alerts

### 5. Document and Train

1. Document alert response procedures
2. Create runbooks for common issues
3. Train QA, Dev, and DevOps teams on alert response
4. Conduct alert response drills

## Conclusion

This monitoring alerts setup provides comprehensive coverage of potential NLP issues in the WhatsApp chatbot system. By integrating with the Debug UI and establishing clear response procedures, the team can quickly identify and resolve issues before they impact users.

The alert thresholds and configurations should be regularly reviewed and adjusted based on real-world performance data and feedback from the QA, Dev, and DevOps teams.

---

*This document should be reviewed and updated regularly as the system evolves and new monitoring requirements are identified.*