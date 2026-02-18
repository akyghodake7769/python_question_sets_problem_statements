import importlib.util
import os
import inspect

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    manager = student_module.ScoreManager()

    print("Running Tests for: Student Score List Operations\n")
    report_lines = ["Running Tests for: Student Score List Operations\n"]

    test_cases = [
        {
            "desc": "Creating score status dictionary",
            "func": "create_status_dict",
            "call": lambda: manager.create_status_dict(),
            "check": lambda result: isinstance(result, dict) and result.get(92) == "Pass" and result.get(45) == "Fail" and len(result) == 8,
            "marks": 2.5
        },
        {
            "desc": "Finding highest score",
            "func": "find_highest_score",
            "call": lambda: manager.find_highest_score(),
            "check": lambda result: result == 95,
            "marks": 2.5
        },
        {
            "desc": "Calculating average score",
            "func": "calculate_average",
            "call": lambda: manager.calculate_average(),
            "check": lambda result: result == 71.5,
            "marks": 2.5
        },
        {
            "desc": "Getting passing scores in descending order",
            "func": "get_passing_scores",
            "call": lambda: manager.get_passing_scores(),
            "check": lambda result: isinstance(result, list) and result == [95, 92, 88],
            "marks": 2.5
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 2.5)
        max_score += marks
        
        try:
            func = getattr(manager, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()

            # Check 1: Pass-only
            if 'pass' in src and len(src) < 80:
                msg = f"FAIL Visible Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                report_lines.append(msg)
                print(msg)
                continue

            # Execute test
            result = case["call"]()

            # Evaluate result
            passed = case["check"](result)
            
            if passed:
                msg = f"PASS Visible Test Case {idx} Passed: {case['desc']}"
                total_score += marks
            else:
                msg = f"FAIL Visible Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"

        except Exception as e:
            msg = f"FAIL Visible Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"

        print(msg)
        report_lines.append(msg)

    # Print total score summary
    score_line = f"\nSCORE: {total_score}/{max_score} (Total)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
