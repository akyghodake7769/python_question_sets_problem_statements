# Java Lab: Resolve Classpath and Dependency Conflicts

Duration : 60 Min.

## Scenario
Identify and resolve classpath and dependency conflicts (Dependency Hell) in a Maven project. You are maintaining a Java application that uses Maven for dependency management. Recently, a developer added a new library, but the application now crashes at runtime (or compilation) due to a dependency conflict. Specifically, a transitive dependency is pulling in an outdated version of a library that clashes with a newer version explicitly required by the project. Your task is to analyze the dependency tree, identify the conflicting library, and use the `<exclusion>` tag in `pom.xml` to remove the outdated transitive dependency so the application compiles and runs successfully.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Run `mvn dependency:tree` to analyze the dependency structure.
- Identify which dependency is pulling in the conflicting transitive library.
- Open `pom.xml` and add an `<exclusion>` block to remove the conflicting dependency.
- Verify the conflict is resolved by running `mvn clean compile`.
- Ensure the application can start without a `NoSuchMethodError` or `ClassNotFoundException`.

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | `pom.xml` has been modified by the student | 4 Marks |
| **TC2** | The `<exclusion>` tag is correctly applied for the conflicting library | 4 Marks |
| **TC3** | `mvn dependency:tree` confirms the conflicting version is removed | 4 Marks |
| **TC4** | Application compiles successfully (`mvn clean compile`) | 4 Marks |
| **TC5** | Application starts successfully (simulated by a clean run execution) | 4 Marks |

**Total Score: 20 Marks**
