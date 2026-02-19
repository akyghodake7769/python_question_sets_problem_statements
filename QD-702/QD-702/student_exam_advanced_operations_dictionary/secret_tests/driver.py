import importlib.util
import os
import sys
from io import StringIO

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    print("Running Tests for: Student Exam Advanced Operations Dictionary\n")
    report_lines = ["Running Tests for: Student Exam Advanced Operations Dictionary\n"]

    test_cases = [
        {
            "desc": "Calculate average score for each student",
            "func": "calculate_student_averages",
            "setup": lambda: student_module.StudentResultManager(),
            "call": lambda obj: obj.calculate_student_averages(),
            "check": lambda output: "Student Averages:" in output and "'S001': 85.0" in output and "'S004': 91.7" in output,
            "marks": 7
        },
        {
            "desc": "Find student with highest average score",
            "func": "find_highest_average",
            "setup": lambda: student_module.StudentResultManager(),
            "call": lambda obj: obj.find_highest_average(),
            "check": lambda output: "Highest Average: Divya (S004) - 91.7" in output,
            "marks": 7
        },
        {
            "desc": "Calculate subject-wise averages",
            "func": "calculate_subject_averages",
            "setup": lambda: student_module.StudentResultManager(),
            "call": lambda obj: obj.calculate_subject_averages(),
            "check": lambda output: "Subject Averages:" in output and "'math': 84.0" in output and "'science': 87.2" in output and "'english': 86.6" in output,
            "marks": 6
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 7)
        is_hidden = case.get("is_hidden", False)
        
        if not is_hidden:
            max_score += marks
        
        try:
            obj = case["setup"]()
            
            # Capture stdout for methods that print
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            try:
                getattr(obj, case["func"])()
                output = sys.stdout.getvalue()
            finally:
                sys.stdout = old_stdout
            
            # Execute test check
            passed = case["check"](output)
            
            if passed:
                test_type = "Hidden" if is_hidden else "Visible"
                msg = f"PASS {test_type} Test Case {idx} Passed: {case['desc']}"
                if not is_hidden:
                    total_score += marks
            else:
                test_type = "Hidden" if is_hidden else "Visible"
                msg = f"FAIL {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"
            
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            test_type = "Hidden" if is_hidden else "Visible"
            msg = f"FAIL {test_type} Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"
            print(msg)
            report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/20.0 (Visible)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
