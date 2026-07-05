# JS_01_M: Resolve Spring Boot Startup Failures

## Objective
Diagnose and resolve startup failures in a Spring Boot application caused by port conflicts and bean wiring errors.

## Problem Description
You are provided with a standard Spring Boot web application. However, when you attempt to start the application, it crashes immediately due to two distinct configuration and code issues:
1. The application attempts to bind to the default port `8080`, which is restricted or occupied in this environment.
2. The application fails with a `NoSuchBeanDefinitionException` because a service dependency could not be found by the Spring container during startup.

Your task is to fix the application so that it compiles and starts successfully in the background, listening on port `8081`.

## Tasks
1. Navigate to the `student_workspace` directory.
2. Modify the code to resolve the Spring Bean wiring error (Hint: Check the `UserService` class).
3. Modify the application configuration to change the server port to `8081`.
4. Ensure the application compiles without errors.
5. Start the application in the background (e.g., `mvn spring-boot:run &`).
6. Ensure the application stays running and the `/actuator/health` endpoint returns a `200 OK` status.

## Evaluation Criteria
- **TC1:** Codebase compiles successfully.
- **TC2:** The missing Spring Stereotype annotation is correctly added to resolve the wiring error.
- **TC3:** `application.properties` is configured to use port `8081`.
- **TC4:** The Java application starts and remains running in the background.
- **TC5:** The `/actuator/health` endpoint is accessible on port `8081` and returns `{ "status": "UP" }`.
