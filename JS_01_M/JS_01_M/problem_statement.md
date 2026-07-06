# JS_01_M: Resolve Spring Boot Startup Failures

**Difficulty Level:** Medium

**Duration:** 60 Minutes

## Scenario

As a Java Developer, you are working on a Spring Boot web application that has been handed over to you in a broken state. The application fails to start due to two distinct problems: a missing Spring stereotype annotation causing a bean wiring error, and a port conflict. Your task is to diagnose and fix these issues so the application runs successfully.

## Task Objectives

Perform the following tasks in the `student_workspace` directory:

### 1. Fix the Spring Bean Wiring Error
- Navigate to `student_workspace/src/main/java/com/kloudlabs/app/service/UserService.java`.
- Add the missing Spring stereotype annotation (`@Service` or `@Component`) to resolve the `NoSuchBeanDefinitionException`.

### 2. Change the Server Port
- Navigate to `student_workspace/src/main/resources/application.properties`.
- Change the server port from the default `8080` to `8081`.

### 3. Compile the Application
- Ensure the project compiles successfully using Maven:
  ```bash
  cd student_workspace
  mvn clean compile
  ```

### 4. Start the Application in the Background
- Start the Spring Boot application in the background:
  ```bash
  cd student_workspace
  nohup mvn spring-boot:run > /tmp/springboot.log 2>&1 &
  ```

### 5. Verify the Actuator Health Endpoint
- Wait 30 seconds for the application to start, then verify it is running:
  ```bash
  curl http://localhost:8081/actuator/health
  ```
- Expected response: `{"status":"UP"}`

## Grading Criteria

| Test Case | Requirement                          | Marks   |
|-----------|--------------------------------------|---------|
| **TC1**   | Maven compile succeeds               | 4 Marks |
| **TC2**   | `@Service` annotation added          | 4 Marks |
| **TC3**   | Port configured to `8081`            | 4 Marks |
| **TC4**   | Application running on port `8081`   | 4 Marks |
| **TC5**   | `/actuator/health` returns `UP`      | 4 Marks |

**Total Score: 20 Marks**

## Important Notes
- Make sure Maven and Java 11+ are installed: `sudo apt-get install maven default-jdk -y`
- The `actuator` dependency must be present in `pom.xml` (it is already included in the starter workspace).
- Run the verification script from the root workspace directory: `python3 student_workspace/run.py`
