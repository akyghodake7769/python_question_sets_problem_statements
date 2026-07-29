# NJS_Q01_E: Event Loop Phase Execution Order
    
## Difficulty: EASY

## Scenario
A Node.js web application is exhibiting runtime anomalies or configuration errors in production. You are tasked with writing clean, async, and correct JavaScript code to solve the requirements.

## Username & Naming Conventions
- Resources must utilize your candidate suffix prefix (`<username>-<exam_code>`).

## Task Objectives
1. **Node.js Optimization & Code Resolution**: Create a script `index.js` that schedules callbacks to log checkpoint strings in a precise order.
2. Ensure your changes pass all local verification tests.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: File index.js exists in workspace** (4 Marks)
- **TC2: Execution returns exit code 0** (4 Marks)
- **TC3: Output sequence matches event loop phase expectations** (4 Marks)
- **TC4: No syntax or runtime errors** (4 Marks)
- **TC5: Verify process.nextTick priority** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
