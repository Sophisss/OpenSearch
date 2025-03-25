# OpenSearch Monitoring 🚨

This guide explains how to configure a **monitor** in OpenSearch that tracks HTTP 500 errors within a specific time frame (last 5 minutes). When the number of errors exceeds a defined threshold, an alert is triggered.

## Overview
This configuration sets up a query-level monitor in OpenSearch to check for HTTP 500 errors in the `logs-demo` index. The monitor runs every minute and checks if the number of errors within the last 5 minutes exceeds a set threshold (in this case, 5 errors). If the threshold is exceeded, an alert is triggered, notifying you of a potential issue with the backend or server.

## Features
- **Query-level monitor**: The monitor queries OpenSearch logs to check the number of HTTP 500 errors in a specific time range (last 5 minutes).
- **Custom alerting**: Alerts are triggered when the number of HTTP 500 errors exceeds a set threshold (e.g., 5 errors in the last 5 minutes).
- **Notification via destination**: Alerts are sent to a configured destination (e.g., email, Slack, etc.).

## Configuration Steps

### 1. OpenSearch Monitor Setup ⚙️
The monitor is set up to query the OpenSearch index `logs-demo` for logs where the `status_code` is `500`. 
The query is executed every minute and checks for errors within the last 5 minutes using the range filter on the `timestamp` field.


#### Query Configuration:
```json
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "status_code": {
              "value": "500"
            }
          }
        },
        {
          "range": {
            "timestamp": {
              "from": "now-5m/m",
              "to": "now/m"
            }
          }
        }
      ]
    }
  }
}
```

### 2. Trigger Condition ⚠️
The trigger condition uses a script to evaluate if the number of 500 errors in the last 5 minutes exceeds the defined threshold (e.g., 5 errors). If the condition is met, an alert is triggered.

#### Example Trigger Condition:
```text
ctx.results[0].hits.total.value > 5
```

If this condition evaluates to `true`, an alert is triggered, indicating that more than 5 HTTP 500 errors have occurred.

### 3. Alerting and Notification 📩
When the trigger condition is met, an alert is sent. The alert contains the following:
- **Subject**: A notification about the high number of HTTP 500 errors.
- **Message**: A warning about the issue, advising the user to check the system logs for potential backend issues.

### 4. OpenSearch Monitor Schedule 🕒
The monitor is scheduled to run every minute `("interval": 1)` and performs the query for HTTP 500 errors from the last 5 minutes.

### 5. Alert Destination 📡
You can configure the alert to be sent to a specific destination (e.g., Slack, email). Ensure that you have a valid destination configured in your OpenSearch alerting setup.

