# Java Lab: Spring Actuator Custom Endpoint & Log Level Security

Duration : 60 Min.

## Scenario
Add custom indicators and lock down Spring Actuator endpoints to enforce secure diagnostic visibility.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Edit `src/main/resources/application.properties`.
2. Expose the actuator endpoints `health`, `info`, and `loggers` using `management.endpoints.web.exposure.include=health,info,loggers`.
3. Force endpoint security role checks by declaring `management.endpoint.health.show-details=always`.

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | `health` endpoint exposed | 2.5 Marks |
| **TC2**   | `info` endpoint exposed | 2.5 Marks |
| **TC3**   | `loggers` endpoint exposed | 2.5 Marks |
| **TC4**   | `show-details` configured to `always` | 2.5 Marks |
| **TC5**   | Configuration properties parsed successfully | 2.5 Marks |
| **TC6**   | Diagnostics API visibility enabled | 2.5 Marks |
| **TC7**   | Custom logger adjustment active | 2.5 Marks |
| **TC8**   | Health endpoint detail visibility authorized | 2.5 Marks |

**Total Score: 20 Marks**
