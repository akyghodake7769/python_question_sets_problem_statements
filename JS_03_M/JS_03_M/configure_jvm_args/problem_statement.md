# Java Lab: Configure JVM Args for Containerised Workloads

Duration : 60 Min.

## Scenario
Configure JVM arguments in a startup script for a Java application running in a containerised environment. You are deploying a Spring Boot application (`app.jar`) into a Linux container. By default, the JVM might not optimally detect the container's memory constraints or use the best garbage collector. You have been provided with a `start.sh` script that currently just runs `java -jar app.jar`. You must update this script to include specific JVM flags to optimize memory and performance.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Edit the `start.sh` script.
- Add the flag `-XX:MaxRAMPercentage=75.0` to ensure the JVM uses 75% of the container's available RAM for the heap.
- Add the flag `-XX:+UseG1GC` to explicitly use the G1 Garbage Collector.
- Ensure the script still correctly executes the `app.jar` in the background (e.g., using `nohup` or `&`).
- Run the script and ensure the Java process remains active in the background.

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | `start.sh` contains the `-XX:MaxRAMPercentage=75.0` flag | 4 Marks |
| **TC2** | `start.sh` contains the `-XX:+UseG1GC` flag | 4 Marks |
| **TC3** | `start.sh` correctly executes the `.jar` file | 4 Marks |
| **TC4** | The Java process successfully starts and remains running | 4 Marks |
| **TC5** | The running Java process actively has the specified flags applied in memory | 4 Marks |

**Total Score: 20 Marks**
