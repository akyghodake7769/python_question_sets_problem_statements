# DB_Q19_M: Multitask Job Pipeline Setup

## Scenario
The candidate must configure the following data operations setup in their workspace environment.

## Username & Naming Conventions
- Candidates must use their normalized username (`<username>`) and exam code (`<exam_code>`) for any resource creation.
- Default resources should follow prefix patterns like `<username>-<exam_code>`.

## Task Objectives
1. **Setup requirements**: Build scheduled multitask pipelines using Task dependencies.
2. Ensure the resources pass standard structural and metadata checks.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: Job layout check** (4 Marks)
- **TC2: Upstream task dependencies definition** (4 Marks)
- **TC3: Parameter parsing validation** (4 Marks)
- **TC4: Task running sequences** (4 Marks)
- **TC5: Failure notification check** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
