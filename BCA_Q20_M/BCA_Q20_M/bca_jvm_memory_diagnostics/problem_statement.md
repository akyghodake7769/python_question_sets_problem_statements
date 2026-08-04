# Basic Code Analysis: JVM Memory OutOfMemoryError Diagnostics

Duration : 90 Min.

## Scenario
Your server crashed with a java.lang.OutOfMemoryError: Java heap space. Analyze the JVM heap memory dump logs and thread logs to find the memory leak.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Document the leak suspect object class name and line number inside 'solution.json'.

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
| **TC2** | Memory leak class suspect correctly identified | 3 Marks |
| **TC3** | Correct list/collection object causing leak identified | 3 Marks |
| **TC4** | Line number of insertion leak mapped correctly | 3 Marks |
| **TC5** | RCA analysis notes populated | 2 Marks |
| **TC6** | Recommended heap memory increase parameter included | 2 Marks |
| **TC7** | Thread dump correlation correct | 2 Marks |
| **TC8** | JVM arguments settings validated | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
