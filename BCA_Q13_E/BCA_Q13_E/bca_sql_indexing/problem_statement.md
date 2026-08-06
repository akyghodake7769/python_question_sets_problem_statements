# Basic Code Analysis: SQL Query Performance & Indexing Analysis

Duration : 30 Min.

## Scenario
A database query on `orders (customer_id, status)` takes 12 seconds due to full table scans. Inspect 'query_plan.txt' and identify the missing index column.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Create/update 'solution.json' inside 'student_workspace/' with fields 'table_name' ('orders') and 'index_column' ('customer_id').

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
| **TC2** | Target table ('orders') identified | 4 Marks |
| **TC3** | Missing index column ('customer_id') identified | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
