# DB_Q21_M: Delta Lake VACUUM & Retention Policy Management

## Scenario
The candidate must configure retention override flags and execute delta log/data VACUUM operations safely on a target Delta table.

## Username & Naming Conventions
- Candidates must use their normalized username (`<username>`) and exam code (`<exam_code>`) for any resource creation.
- Default resources should follow prefix patterns like `<username>-<exam_code>`.

## Task Objectives
1. **Setup requirements**: Configure zero-retention parameters and run VACUUM command to purge stale data files.
2. Ensure Spark configurations allow zero-retention values (`spark.databricks.delta.vacuum.invalidRetentionDurationCheck.enabled = false`).
3. Run `VACUUM` to clean up stale files.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: Table existence verification** (4 Marks)
- **TC2: Override configuration check (invalidRetentionDurationCheck disable)** (4 Marks)
- **TC3: VACUUM execution check** (4 Marks)
- **TC4: Purged data files verification** (4 Marks)
- **TC5: Table history metadata retention check** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
