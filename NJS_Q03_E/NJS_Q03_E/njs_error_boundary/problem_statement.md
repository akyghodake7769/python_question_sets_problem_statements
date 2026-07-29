# NJS_Q03_E: Express.js Exception Boundaries
    
## Difficulty: EASY

## Scenario
A Node.js web application is exhibiting runtime anomalies or configuration errors in production. You are tasked with writing clean, async, and correct JavaScript code to solve the requirements.

## Username & Naming Conventions
- Resources must utilize your candidate suffix prefix (`<username>-<exam_code>`).

## Task Objectives
1. **Node.js Optimization & Code Resolution**: Set up global process listeners for uncaughtException/unhandledRejection and wrap routes in an error boundary.
2. Ensure your changes pass all local verification tests.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: File server.js exists in workspace** (4 Marks)
- **TC2: Global uncaughtException listener registered** (4 Marks)
- **TC3: Global unhandledRejection listener registered** (4 Marks)
- **TC4: Express error middleware handles async exceptions** (4 Marks)
- **TC5: Application shuts down gracefully on uncaught exceptions** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
