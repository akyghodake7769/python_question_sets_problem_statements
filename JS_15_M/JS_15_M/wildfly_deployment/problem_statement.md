# Java Lab: JBoss / WildFly Standalone App Server Deployment

Duration : 60 Min.

## Scenario
Configure standalone server listener port bindings inside WildFly configuration directories.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate `configuration/standalone.xml`.
2. Configure the HTTP socket binding port setting to offset default port listening parameters from `8080` to `8082`:
   `<socket-binding name="http" port="8082"/>`

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | `configuration/standalone.xml` exists | 2.5 Marks |
| **TC2**   | HTTP port set to `8082` | 2.5 Marks |
| **TC3**   | XML structure is parsed correctly | 2.5 Marks |
| **TC4**   | WildFly server port offset configuration active | 2.5 Marks |
| **TC5**   | HTTP interface listener registered | 2.5 Marks |
| **TC6**   | Standalone profile deployment context valid | 2.5 Marks |
| **TC7**   | Bindings socket offset configured | 2.5 Marks |
| **TC8**   | HTTP routing socket parameters enabled | 2.5 Marks |

**Total Score: 20 Marks**
