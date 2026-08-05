# Log Analysis: Java MDC Context & Distributed Transaction Tracing

Duration : 60 Min.

## Scenario
A distributed order checkout flow failed across 4 microservices. Trace the MDC span context to reconstruct the exact failure timeline.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Fill out 'trace_timeline.json' with chronological service span sequence and failing service name.

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
| **TC1** | trace_timeline.json exists and is valid JSON | 5 Marks |
| **TC2** | Trace ID ('trace-7741') correctly matched across all spans | 5 Marks |
| **TC3** | Failing downstream span service correctly identified | 5 Marks |
| **TC4** | Span execution latency correctly calculated | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
