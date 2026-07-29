# NJS_Q06_M: Memory Leak Diagnostics
    
## Difficulty: MEDIUM

## Scenario
A Node.js web application is exhibiting runtime anomalies or configuration errors in production. You are tasked with writing clean, async, and correct JavaScript code to solve the requirements.

## Username & Naming Conventions
- Resources must utilize your candidate suffix prefix (`<username>-<exam_code>`).

## Task Objectives
1. **Node.js Optimization & Code Resolution**: Diagnose and patch a memory leak caused by unbounded array accumulation in Express route handlers.
2. Ensure your changes pass all local verification tests.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: File server.js exists in workspace** (4 Marks)
- **TC2: Memory leak diagnostic report created** (4 Marks)
- **TC3: Leaking array resolved or replaced with size-limited collection** (4 Marks)
- **TC4: Express routes perform successfully under load** (4 Marks)
- **TC5: Memory heap consumption verified to remain bounded** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
