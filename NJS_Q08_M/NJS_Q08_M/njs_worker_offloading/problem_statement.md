# NJS_Q08_M: Sync Offloading / Worker Pool
    
## Difficulty: MEDIUM/HARD

## Scenario
A Node.js web application is exhibiting runtime anomalies or configuration errors in production. You are tasked with writing clean, async, and correct JavaScript code to solve the requirements.

## Username & Naming Conventions
- Resources must utilize your candidate suffix prefix (`<username>-<exam_code>`).

## Task Objectives
1. **Node.js Optimization & Code Resolution**: Offload a CPU-bound hashing workload from the main event loop using worker_threads.
2. Ensure your changes pass all local verification tests.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: File server.js exists in workspace** (4 Marks)
- **TC2: File worker.js exists in workspace** (4 Marks)
- **TC3: Worker pools utilized for processing CPU-intensive operations** (4 Marks)
- **TC4: Main execution threads remain non-blocked during hashing execution** (4 Marks)
- **TC5: Asynchronous response payloads correctly formatted** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
