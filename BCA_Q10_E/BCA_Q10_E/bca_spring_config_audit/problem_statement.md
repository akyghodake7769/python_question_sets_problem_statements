# Basic Code Analysis: Auditing Spring properties files

Duration : 30 Min.

## Scenario
A Spring Boot microservice fails to run in Dev environment because database profiles are mismatched. Audit the config files.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Correct active profile properties and database URLs inside 'application.properties'.

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
| **TC1** | application.properties has valid Spring boot keys | 3 Marks |
| **TC2** | Active profile set to 'dev' | 4 Marks |
| **TC3** | Database URL port set to local container port 3306 | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
