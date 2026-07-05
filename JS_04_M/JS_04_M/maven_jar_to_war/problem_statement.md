# JS_04_M: Maven Artefacts (JAR to WAR Conversion)

## Objective
Identify Maven build artefacts and successfully alter the deployment format from a standalone `jar` to a deployable `war` archive.

## Problem Description
You have a standard Spring Boot application configured to build as an executable `jar` file with an embedded Tomcat server. The infrastructure team has requested that this application be deployed to an external, standalone Tomcat application server.

To achieve this, you must modify the `pom.xml` file to build a `.war` file instead of a `.jar` file, and ensure that the embedded Tomcat dependencies do not interfere with the external server.

## Tasks
1. Navigate to the `student_workspace` directory.
2. Open the `pom.xml` file.
3. Change the packaging type of the Maven project to `war`.
4. Add the `spring-boot-starter-tomcat` dependency, but specifically mark its scope as `provided` so it is not bundled inside the final `.war` file.
5. Run `mvn clean package` to build the project.
6. Verify that a valid `.war` file is generated in the `target/` directory.

## Evaluation Criteria
- **TC1:** `<packaging>war</packaging>` is correctly set in `pom.xml`.
- **TC2:** The `spring-boot-starter-tomcat` dependency is added with `<scope>provided</scope>`.
- **TC3:** `mvn clean package` executes successfully without compilation errors.
- **TC4:** A `.war` file is successfully generated in the `target/` directory.
- **TC5:** The generated `.war` file is a valid archive (checked internally by the driver).
