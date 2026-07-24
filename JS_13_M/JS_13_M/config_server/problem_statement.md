# Java Lab: Spring Cloud Config Server Integration

Duration : 60 Min.

## Scenario
Configure a centralized config client to fetch property structures from a Git-backed Config Server.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate `src/main/resources/bootstrap.yml`.
2. Configure config client properties to point to config server URL `http://localhost:8888` and fetch application overrides:
   `spring.cloud.config.uri=http://localhost:8888`
   `spring.cloud.config.name=ops-app`

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | `spring.cloud.config.uri` set to `http://localhost:8888` | 2.5 Marks |
| **TC2**   | Config server client name set to `ops-app` | 2.5 Marks |
| **TC3**   | Client configuration loaded correctly | 2.5 Marks |
| **TC4**   | Application context resolution active | 2.5 Marks |
| **TC5**   | Client config format parsed | 2.5 Marks |
| **TC6**   | Central credentials fetch enabled | 2.5 Marks |
| **TC7**   | Spring cloud bootstrap parameters registered | 2.5 Marks |
| **TC8**   | Remote config lookup precedence validated | 2.5 Marks |

**Total Score: 20 Marks**
