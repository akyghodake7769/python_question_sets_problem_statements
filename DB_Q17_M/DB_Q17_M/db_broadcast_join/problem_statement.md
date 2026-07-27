# DB_Q17_M: Spark Broadcast Join Optimization

## Scenario
The candidate must configure the following data operations setup in their workspace environment.

## Username & Naming Conventions
- Candidates must use their normalized username (`<username>`) and exam code (`<exam_code>`) for any resource creation.
- Default resources should follow prefix patterns like `<username>-<exam_code>`.

## Task Objectives
1. **Setup requirements**: Optimize PySpark lookup join operations using broadcast flags.
2. Ensure the resources pass standard structural and metadata checks.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: Join outcome correctness** (4 Marks)
- **TC2: Broadcast hint check in AST** (4 Marks)
- **TC3: Optimization execution check** (4 Marks)
- **TC4: Query plan metrics validation** (4 Marks)
- **TC5: Output schema structure check** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
