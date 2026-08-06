# Basic Code Analysis: Spotting Logical & Null Errors

Duration : 30 Min.

## Scenario
An application is crashing with a Null Pointer / Undefined Exception when looking up non-existent user IDs. Create and implement a safe lookup module in student_workspace/.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/user_lookup.js`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Create a file named 'user_lookup.js' directly inside 'student_workspace/'. Implement the 'getUserEmail(user)' function ensuring it safely handles null/undefined user objects.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect the scenario input files in `student_workspace/`.
3. Create/update the file `student_workspace/user_lookup.js` and populate it with valid parameters and configurations.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your work by running `python run.py` in the terminal before submitting.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | user_lookup.js exists in student_workspace/ with valid JS code | 3 Marks |
| **TC2** | Code handles non-existent/null user objects correctly | 4 Marks |
| **TC3** | Function returns empty string or null instead of throwing error | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
