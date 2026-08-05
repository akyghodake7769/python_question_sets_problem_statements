# Log Analysis: Automated Error Clustering & Signature Libraries

Duration : 90 Min.

## Scenario
You need to write a Python script that reads raw application logs, normalizes stack trace signatures, clusters identical errors, and matches them to runbook entries.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Complete the Python script 'cluster_errors.py' to produce 'error_clusters.json'.

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
| **TC1** | cluster_errors.py is syntax-valid Python | 3 Marks |
| **TC2** | Parses error logs and normalizes dynamic IDs/timestamps | 3 Marks |
| **TC3** | Groups identical error signatures into clusters | 3 Marks |
| **TC4** | Writes structured JSON output to error_clusters.json | 3 Marks |
| **TC5** | Matches cluster signature to runbook ID | 2 Marks |
| **TC6** | Calculates error frequency per cluster | 2 Marks |
| **TC7** | Handles missing/malformed log lines gracefully | 2 Marks |
| **TC8** | Includes first and last occurrence timestamps | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
