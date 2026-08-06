# Basic Code Analysis: Cache Invalidation & TTL Eviction Logic

Duration : 30 Min.

## Scenario
Users report seeing stale product prices after catalog updates. Create 'cache_service.py' in student_workspace/ and add a cache eviction call upon product updates.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/cache_service.py`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Create 'cache_service.py' inside 'student_workspace/'. Implement 'redis_client.delete(f"product:{product_id}")' during price updates.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect the scenario input files in `student_workspace/`.
3. Create/update the file `student_workspace/cache_service.py` and populate it with valid parameters and configurations.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your work by running `python run.py` in the terminal before submitting.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | cache_service.py exists in student_workspace/ with valid Python code | 3 Marks |
| **TC2** | Cache deletion / invalidation call added | 4 Marks |
| **TC3** | Key pattern 'product:{id}' invalidated | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
