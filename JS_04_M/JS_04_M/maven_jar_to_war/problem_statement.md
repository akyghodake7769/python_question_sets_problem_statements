# Java Lab: Maven Artefacts (JAR to WAR Conversion)

Duration : 60 Min.

## Scenario
Identify Maven build artefacts and successfully alter the deployment format from a standalone `jar` to a deployable `war` archive. You have a standard Spring Boot application configured to build as an executable `jar` file with an embedded Tomcat server. The infrastructure team has requested that this application be deployed to an external, standalone Tomcat application server. To achieve this, you must modify the `pom.xml` file to build a `.war` file instead of a `.jar` file, and ensure that the embedded Tomcat dependencies do not interfere with the external server.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Open the `pom.xml` file.
- Change the packaging type of the Maven project to `war`.
- Add the `spring-boot-starter-tomcat` dependency, but specifically mark its scope as `provided` so it is not bundled inside the final `.war` file.
- Run `mvn clean package` to build the project.
- Verify that a valid `.war` file is generated in the `target/` directory.

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | `<packaging>war</packaging>` is correctly set in `pom.xml` | 4 Marks |
| **TC2** | The `spring-boot-starter-tomcat` dependency is added with `<scope>provided</scope>` | 4 Marks |
| **TC3** | `mvn clean package` executes successfully without compilation errors | 4 Marks |
| **TC4** | A `.war` file is successfully generated in the `target/` directory | 4 Marks |
| **TC5** | The generated `.war` file is a valid archive | 4 Marks |

**Total Score: 20 Marks**
