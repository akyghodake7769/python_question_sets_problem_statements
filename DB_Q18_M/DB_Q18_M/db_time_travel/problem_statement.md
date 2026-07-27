# DB_Q18_M: Delta Lake Time Travel & Restore

## Scenario
The candidate must configure the following data operations setup in their workspace environment.

## Username & Naming Conventions
- Candidates must use their normalized username (`<username>`) and exam code (`<exam_code>`) for any resource creation.
- Default resources should follow prefix patterns like `<username>-<exam_code>`.

## Task Objectives
1. **Setup requirements**: Restore a Delta table to a previous history version state.
2. Ensure the resources pass standard structural and metadata checks.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: Version check validation** (4 Marks)
- **TC2: Restore query execution** (4 Marks)
- **TC3: Row count matching** (4 Marks)
- **TC4: Data consistency check** (4 Marks)
- **TC5: History logs presence** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
