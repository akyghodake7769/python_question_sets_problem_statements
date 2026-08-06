# Basic Code Analysis: System Metrics & Resource Utilization Triage

Duration : 30 Min.

## Scenario
A Linux server experienced an Out-Of-Memory (OOM) kill event. Inspect 'sysstat.log' and identify the process name killed by OOM killer.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Create/update 'solution.json' inside 'student_workspace/' with fields 'killed_process' ('java_app') and 'pid' (4891).

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect the scenario input files in `student_workspace/`.
3. Create/update the file `student_workspace/solution.json` and populate it with valid parameters and configurations.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your work by running `python run.py` in the terminal before submitting.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | solution.json exists in student_workspace/ | 3 Marks |
| **TC2** | Killed process name ('java_app') identified | 4 Marks |
| **TC3** | PID (4891) correctly extracted | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
