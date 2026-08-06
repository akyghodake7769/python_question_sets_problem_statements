# Basic Code Analysis: Environment Variable & Secrets Injection Audit

Duration : 30 Min.

## Scenario
Hardcoded database credentials ('DB_PASSWORD=secret123') were found in source code. Create 'config.js' in student_workspace/ reading credentials from environment variables.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/config.js`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Create 'config.js' inside 'student_workspace/'. Replace hardcoded password strings with 'process.env.DB_PASSWORD'.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect the scenario input files in `student_workspace/`.
3. Create/update the file `student_workspace/config.js` and populate it with valid parameters and configurations.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your work by running `python run.py` in the terminal before submitting.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | config.js exists in student_workspace/ with valid JS code | 3 Marks |
| **TC2** | Hardcoded secret string removed | 4 Marks |
| **TC3** | process.env.DB_PASSWORD environment variable referenced | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
