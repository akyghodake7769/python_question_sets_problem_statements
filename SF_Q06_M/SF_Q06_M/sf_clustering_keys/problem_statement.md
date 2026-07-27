# SF_Q06_M: Snowflake Clustering Keys Optimization

## Scenario
The candidate must configure the following data operations setup in their workspace environment.

## Username & Naming Conventions
- Candidates must use their normalized username (`<username>`) and exam code (`<exam_code>`) for any resource creation.
- Default resources should follow prefix patterns like `<username>-<exam_code>`.

## Task Objectives
1. **Setup requirements**: Configure clustering keys on large tables and verify pruning details.
2. Ensure the resources pass standard structural and metadata checks.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: Clustering key verification** (4 Marks)
- **TC2: Micro-partition depth check** (4 Marks)
- **TC3: Performance query execution** (4 Marks)
- **TC4: Database catalog metadata check** (4 Marks)
- **TC5: Query plan metrics check** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
