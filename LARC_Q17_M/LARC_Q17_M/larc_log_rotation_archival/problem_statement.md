# Log Analysis: Log Rotation Audit & Compressed Log Archival Triage

Duration : 90 Min.

## Scenario
An incident occurred yesterday, but active log files were rotated and compressed (`syslog.2.gz`). Use Linux `zgrep` / `zcat` tools to locate the error trace.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Document the rotated log archive details inside 'solution.json'.

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
| **TC1** | solution.json exists | 3 Marks |
| **TC2** | Target compressed archive file ('syslog.2.gz') correctly identified | 3 Marks |
| **TC3** | Timestamp of initial rotated failure extracted | 3 Marks |
| **TC4** | Error exception class identified | 3 Marks |
| **TC5** | zgrep filter expression documented | 2 Marks |
| **TC6** | Log rotation policy type identified (size/daily) | 2 Marks |
| **TC7** | Impacted service process ID matched | 2 Marks |
| **TC8** | Root cause summary filled | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
