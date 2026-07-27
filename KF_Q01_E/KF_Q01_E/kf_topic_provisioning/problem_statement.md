# KF_Q01_E: Kafka Topic Provisioning

## Scenario
The candidate must configure the following data operations setup in their workspace environment.

## Username & Naming Conventions
- Candidates must use their normalized username (`<username>`) and exam code (`<exam_code>`) for any resource creation.
- Default resources should follow prefix patterns like `<username>-<exam_code>`.

## Task Objectives
1. **Setup requirements**: Provision topics with partitions and replication specifications.
2. Ensure the resources pass standard structural and metadata checks.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: Topic existence (telemetry-stream)** (4 Marks)
- **TC2: Partition count check (3)** (4 Marks)
- **TC3: Replication factor verification (1)** (4 Marks)
- **TC4: Reserved validation** (4 Marks)
- **TC5: Reserved validation** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
