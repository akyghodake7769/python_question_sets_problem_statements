# Basic Code Analysis: Security Audit of Hardcoded Credentials

Duration : 60 Min.

## Scenario
Conduct a security audit across source code files. Extract hardcoded JWT secret tokens, AWS keys, and database passwords into 'security_audit.json'.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/security_audit.json`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Create/update 'security_audit.json' inside 'student_workspace/' with fields 'aws_access_key', 'jwt_secret', and 'remediation'.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect the scenario input files in `student_workspace/`.
3. Create/update the file `student_workspace/security_audit.json` and populate it with valid parameters and configurations.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your work by running `python run.py` in the terminal before submitting.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | security_audit.json exists in student_workspace/ and is valid JSON | 5 Marks |
| **TC2** | Hardcoded AWS Access Key identified | 5 Marks |
| **TC3** | Hardcoded JWT secret token identified | 5 Marks |
| **TC4** | Remediation recommendation provided | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
