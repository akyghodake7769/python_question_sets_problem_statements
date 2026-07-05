# JS_05_M: Resolve Classpath and Dependency Conflicts

## Objective
Identify and resolve classpath and dependency conflicts (Dependency Hell) in a Maven project.

## Problem Description
You are maintaining a Java application that uses Maven for dependency management. Recently, a developer added a new library, but the application now crashes at runtime (or compilation) due to a dependency conflict. 

Specifically, a transitive dependency is pulling in an outdated version of a library that clashes with a newer version explicitly required by the project.

Your task is to analyze the dependency tree, identify the conflicting library, and use the `<exclusion>` tag in `pom.xml` to remove the outdated transitive dependency so the application compiles and runs successfully.

## Tasks
1. Navigate to the `student_workspace` directory.
2. Run `mvn dependency:tree` to analyze the dependency structure.
3. Identify which dependency is pulling in the conflicting transitive library.
4. Open `pom.xml` and add an `<exclusion>` block to remove the conflicting dependency.
5. Verify the conflict is resolved by running `mvn clean compile`.
6. Ensure the application can start without a `NoSuchMethodError` or `ClassNotFoundException`.

## Evaluation Criteria
- **TC1:** `pom.xml` has been modified by the student.
- **TC2:** The `<exclusion>` tag is correctly applied for the conflicting library.
- **TC3:** `mvn dependency:tree` confirms the conflicting version is removed.
- **TC4:** Application compiles successfully (`mvn clean compile`).
- **TC5:** Application starts successfully (simulated by a clean run execution).
