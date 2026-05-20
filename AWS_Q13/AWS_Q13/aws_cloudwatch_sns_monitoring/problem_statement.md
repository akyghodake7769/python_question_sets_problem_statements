# DevOps Lab: AWS CloudWatch Monitoring & Automated SNS Alerting

**Difficulty Level:** Medium  
**Duration:** 60 Minutes

## Scenario

An organization requires automated monitoring and alerting for their cloud compute infrastructure to ensure high availability and prevent service outages. Currently, system administrators manually check server metrics, which results in delayed incident response when CPU spikes occur. To establish a robust Site Reliability Engineering (SRE) practice, the team requires an automated CloudWatch monitoring and SNS alerting architecture. The learner will provision an EC2 instance attached to an IAM Instance Profile, create an Amazon SNS topic for DevOps alerts, and configure an Amazon CloudWatch Alarm that monitors CPU utilization and triggers email notifications during high load events.

## Requirements

The learner must:

- Provision an AWS EC2 instance named `labskraft-monitor-ec2-<your-labskraft-username>` attached to a dedicated IAM Role / Instance Profile.
- Create an Amazon SNS Topic named `DevOps-Alerts-<your-labskraft-username>` and subscribe an active email address to receive notifications.
- Configure an Amazon CloudWatch Alarm named `High-CPU-Alarm` that:
  - Monitors the `CPUUtilization` metric of the provisioned EC2 instance.
  - Sets the threshold condition to trigger when CPU exceeds **70%** for 1 evaluation period of 5 minutes (`Period=300`).
  - Configures the Alarm Action to publish notifications to the destination SNS topic.
- Ensure the alarm is correctly configured and transitions to the `OK` state (or `ALARM` state when stress tested).

## Expected Workflow

```text
EC2 Instance Execution
      ↓
CloudWatch Metric (CPUUtilization > 70%)
      ↓
CloudWatch Alarm Trigger (High-CPU-Alarm)
      ↓
SNS Topic Action (DevOps-Alerts)
      ↓
Automated Email Alert Delivery
```

## Sample Evaluation Report

Your setup should generate a state verification log similar to the following:

```text
EC2_IAM_PROFILE=SUCCESS
SNS_TOPIC_CONFIGURED=SUCCESS
CLOUDWATCH_ALARM_ENABLED=SUCCESS
ALARM_THRESHOLD=70
FINAL_STATUS=SUCCESS
TIMESTAMP=Thu May 15 10:15:30 UTC 2026
```

## Deliverables

The final solution should include:

| Deliverable                         | Description                      |
| ----------------------------------- | -------------------------------- |
| **EC2 Instance & IAM**        | Monitored compute resource       |
| **Amazon SNS Topic**          | Notification delivery hub        |
| **CloudWatch Alarm**          | Metric threshold monitor         |

## Technology Stack

| Technology                | Purpose                 |
| ------------------------- | ----------------------- |
| **AWS EC2 & IAM**         | Compute & Identity      |
| **AWS CloudWatch**        | Monitoring & Alarms     |
| **AWS SNS**               | Pub/Sub Alerting        |

## Verification & Grading Criteria

Your performance will be automatically evaluated based on the following test cases.

| Test Case     | Requirement                            | Validation                                                | Marks    |
| ------------- | -------------------------------------- | --------------------------------------------------------- | -------- |
| **TC1** | **EC2 Instance & IAM Setup**     | EC2 instance exists with IAM Instance Profile attached    | 10 Marks |
| **TC2** | **Amazon SNS Topic Setup**       | SNS Topic exists with active/pending email subscription   | 10 Marks |
| **TC3** | **CloudWatch Alarm Configuration**| CloudWatch Alarm exists for CPU >70% linked to SNS topic  | 10 Marks |

**Total Score: 30 Marks**
