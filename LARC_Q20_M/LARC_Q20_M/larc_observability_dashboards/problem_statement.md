# Log Analysis: Dashboard Panel Visualizations & Health Metrics

Duration : 90 Min.

## Scenario
Design an observability dashboard layout containing field-based visualizations for error rate, throughput, transaction latency, and service health status.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Fill out 'dashboard_config.json' detailing panel queries and visualization types.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | dashboard_config.json exists | 3 Marks |
| **TC2** | Error rate panel query and timeseries chart configured | 3 Marks |
| **TC3** | Throughput panel (requests per minute) configured | 3 Marks |
| **TC4** | Latency heatmap / bar chart panel configured | 3 Marks |
| **TC5** | Service health status gauge panel included | 2 Marks |
| **TC6** | Alert notification channel mapped | 2 Marks |
| **TC7** | Auto-refresh interval set to 30s/1m | 2 Marks |
| **TC8** | Dashboard grid layout coordinates specified | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
