# Java Lab: Graceful Shutdown & Kubernetes PreStop Hooks

Duration : 60 Min.

## Scenario
Configure a Spring Boot application and a Kubernetes lifecycle pre-stop hook to execute graceful connection draining.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate `src/main/resources/application.properties`.
2. Configure graceful shutdown and termination timeout properties:
   `server.shutdown=graceful`
   `spring.lifecycle.timeout-per-shutdown-phase=30s`
3. Edit `pre-stop.sh` in the root workspace directory. Add a curl trigger command to wait/sleep for `10` seconds during container termination:
   `sleep 10`

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | `server.shutdown=graceful` configured | 2.5 Marks |
| **TC2**   | `spring.lifecycle.timeout-per-shutdown-phase=30s` configured | 2.5 Marks |
| **TC3**   | `pre-stop.sh` script exists | 2.5 Marks |
| **TC4**   | `pre-stop.sh` contains the `sleep 10` command | 2.5 Marks |
| **TC5**   | Script and configuration syntax valid | 2.5 Marks |
| **TC6**   | In-flight request draining enabled | 2.5 Marks |
| **TC7**   | Shutdown phase timeout active | 2.5 Marks |
| **TC8**   | Kubernetes preStop duration mapped | 2.5 Marks |

**Total Score: 20 Marks**
