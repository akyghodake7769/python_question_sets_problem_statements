# JS_03_M: Configure JVM Args for Containerised Workloads

## Objective
Configure JVM arguments in a startup script for a Java application running in a containerised environment.

## Problem Description
You are deploying a Spring Boot application (`app.jar`) into a Linux container. By default, the JVM might not optimally detect the container's memory constraints or use the best garbage collector. 

You have been provided with a `start.sh` script that currently just runs `java -jar app.jar`. You must update this script to include specific JVM flags to optimize memory and performance.

## Tasks
1. Navigate to the `student_workspace` directory.
2. Edit the `start.sh` script.
3. Add the flag `-XX:MaxRAMPercentage=75.0` to ensure the JVM uses 75% of the container's available RAM for the heap.
4. Add the flag `-XX:+UseG1GC` to explicitly use the G1 Garbage Collector.
5. Ensure the script still correctly executes the `app.jar` in the background (e.g., using `nohup` or `&`).
6. Run the script and ensure the Java process remains active in the background.

## Evaluation Criteria
- **TC1:** `start.sh` contains the `-XX:MaxRAMPercentage=75.0` flag.
- **TC2:** `start.sh` contains the `-XX:+UseG1GC` flag.
- **TC3:** `start.sh` correctly executes the `.jar` file.
- **TC4:** The Java process successfully starts and remains running.
- **TC5:** The running Java process actively has the specified flags applied in memory (verified via `ps`).
