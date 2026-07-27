# DB_Q20_M: Spark Z-Ordering & Partitioning

## Scenario
The candidate must configure the following data operations setup in their workspace environment.

## Username & Naming Conventions
- Candidates must use their normalized username (`<username>`) and exam code (`<exam_code>`) for any resource creation.
- Default resources should follow prefix patterns like `<username>-<exam_code>`.

## Task Objectives
1. **Setup requirements**: Perform partitioning and Z-Order optimization on target dimensions.
2. Ensure the resources pass standard structural and metadata checks.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: Partition layout check** (4 Marks)
- **TC2: Z-order layout metadata check** (4 Marks)
- **TC3: Query run metrics check** (4 Marks)
- **TC4: Compaction optimization index** (4 Marks)
- **TC5: Pruning evaluation check** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
