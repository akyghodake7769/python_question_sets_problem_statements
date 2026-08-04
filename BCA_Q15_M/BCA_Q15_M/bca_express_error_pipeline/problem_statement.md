# Basic Code Analysis: Custom Express Middleware Error Pipelines

Duration : 60 Min.

## Scenario
Your Express server leaks raw database stack traces to clients during exceptions. Implement a custom error-handling middleware to sanitize error payloads.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Write error-handling middleware function in 'app.js' with signature (err, req, res, next) returning status 500.

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
| **TC1** | Custom middleware function declared with 4 arguments | 5 Marks |
| **TC2** | Sanitizes raw SQL queries from the client error response | 5 Marks |
| **TC3** | Logs raw details locally to file/console | 5 Marks |
| **TC4** | Sends formatted JSON client response with public message | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
