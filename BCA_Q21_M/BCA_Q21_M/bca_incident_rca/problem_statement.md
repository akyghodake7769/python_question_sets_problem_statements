# Basic Code Analysis: Root Cause Analysis of Production Outage

Duration : 60 Min.

## Scenario
A major production outage occurred during peak hours. Perform a complete RCA by auditing Git commits and application logs. Document findings in 'outage_rca.json'.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/outage_rca.json`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Create/update 'outage_rca.json' inside 'student_workspace/' with fields 'rca_commit_hash', 'trigger_exception', and 'prevention_plan'.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
2. Initialize the repository history by running:
   `python setup_git.py`
3. Use Git CLI tools in the terminal to inspect the commit history.
4. Create/update `student_workspace/outage_rca.json` and record the extracted commit hash and author username.
5. Save your changes (`Ctrl + S` or `Cmd + S`).
6. Verify your work by running `python run.py` in the terminal before submitting.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | outage_rca.json exists in student_workspace/ and is valid JSON | 5 Marks |
| **TC2** | Root cause commit hash identified | 5 Marks |
| **TC3** | Triggering error exception class identified | 5 Marks |
| **TC4** | Long-term prevention plan documented | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
