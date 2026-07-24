# Java Lab: Connection Pool Sizing and Saturated Latency

Duration : 60 Min.

## Scenario
Optimize HikariCP database connection pooling parameters inside `application.properties` to ensure maximum concurrency and prevent request timeouts.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Open `src/main/resources/application.properties`.
2. Configure the following pool limits:
   - `spring.datasource.hikari.maximum-pool-size=50`
   - `spring.datasource.hikari.connection-timeout=15000`
   - `spring.datasource.hikari.minimum-idle=10`
   - `spring.datasource.hikari.idle-timeout=600000`

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | `spring.datasource.hikari.maximum-pool-size=50` configured | 2.5 Marks |
| **TC2**   | `spring.datasource.hikari.connection-timeout=15000` configured | 2.5 Marks |
| **TC3**   | `spring.datasource.hikari.minimum-idle=10` configured | 2.5 Marks |
| **TC4**   | `spring.datasource.hikari.idle-timeout=600000` configured | 2.5 Marks |
| **TC5**   | Configuration contains no syntax/parsing errors | 2.5 Marks |
| **TC6**   | Pool settings are active and load correctly | 2.5 Marks |
| **TC7**   | Connection timeouts set under the maximum allowed threshold | 2.5 Marks |
| **TC8**   | Min-idle capacity configured for background performance | 2.5 Marks |

**Total Score: 20 Marks**
