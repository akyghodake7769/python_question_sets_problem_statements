# Basic Code Analysis: Advanced Incident RCA Audit Logging

Duration : 90 Min.

## Scenario
Analyze a multi-system failure involving a network gateway timeout and a database deadlock, classify the issues, and generate a structured post-mortem log.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Fill out 'rca_audit_log.json' detailing the incident correlation timeline and classification category.

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
| **TC1** | rca_audit_log.json exists and is valid JSON | 3 Marks |
| **TC2** | Primary classification mapped to INTEGRATION/INFRA | 3 Marks |
| **TC3** | Deadlock trigger transaction correctly identified | 3 Marks |
| **TC4** | Gateway timeout duration correctly calculated | 3 Marks |
| **TC5** | Correlation ID matched | 2 Marks |
| **TC6** | Post-mortem timeline entries are sequential | 2 Marks |
| **TC7** | Mitigation steps are documented | 2 Marks |
| **TC8** | Severity level correctly identified | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
