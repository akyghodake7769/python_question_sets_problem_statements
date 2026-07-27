# SF_Q03_E: Snowflake Schema Ingestion

## Scenario
The candidate must configure the following data operations setup in their workspace environment.

## Username & Naming Conventions
- Candidates must use their normalized username (`<username>`) and exam code (`<exam_code>`) for any resource creation.
- Default resources should follow prefix patterns like `<username>-<exam_code>`.

## Task Objectives
1. **Setup requirements**: Setup administrative database, schema, and raw log tables.
2. Ensure the resources pass standard structural and metadata checks.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: Database existence (admin_db)** (4 Marks)
- **TC2: Schema existence (raw)** (4 Marks)
- **TC3: Table columns structure** (4 Marks)
- **TC4: Reserved validation** (4 Marks)
- **TC5: Reserved validation** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
