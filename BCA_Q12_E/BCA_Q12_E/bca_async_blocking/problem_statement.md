# Basic Code Analysis: Async/Await & Thread Blocking Analysis

Duration : 30 Min.

## Scenario
A Node.js event loop freezes because synchronous `fs.readFileSync` is used inside an HTTP handler. Create 'app.js' in student_workspace/ using asynchronous `fs.promises.readFile`.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/app.js`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Create 'app.js' inside 'student_workspace/'. Implement 'handleRequest' using async/await with 'fs.promises.readFile'.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect the scenario input files in `student_workspace/`.
3. Create/update the file `student_workspace/app.js` and populate it with valid parameters and configurations.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your work by running `python run.py` in the terminal before submitting.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | app.js exists in student_workspace/ with valid JS code | 3 Marks |
| **TC2** | readFileSync removed from handler | 4 Marks |
| **TC3** | async/await or promises readFile implemented | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
