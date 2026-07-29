# NJS_Q05_E: Event Loop Latency Monitor
    
## Difficulty: EASY

## Scenario
A Node.js web application is exhibiting runtime anomalies or configuration errors in production. You are tasked with writing clean, async, and correct JavaScript code to solve the requirements.

## Username & Naming Conventions
- Resources must utilize your candidate suffix prefix (`<username>-<exam_code>`).

## Task Objectives
1. **Node.js Optimization & Code Resolution**: Implement an event loop lag tracking helper using perf_hooks to alert on latency spikes.
2. Ensure your changes pass all local verification tests.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: File monitor.js exists in workspace** (4 Marks)
- **TC2: Module imports monitorEventLoopDelay from perf_hooks** (4 Marks)
- **TC3: Latency monitoring helper class or function implemented** (4 Marks)
- **TC4: Lag threshold triggers custom alerts or logs** (4 Marks)
- **TC5: Statistics reports 95th percentile metrics successfully** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
