import importlib.util
import os

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    print("Running Tests for: Online Course Manager\n")
    report_lines = ["Running Tests for: Online Course Manager\n"]

    test_cases = [
        {
            "desc": "Initialize manager structure",
            "func": "initialize",
            "setup": lambda: student_module.CourseManager(),
            "call": lambda obj: obj.courses,
            "check": lambda result: isinstance(result, dict) and len(result) == 0,
            "marks": 5
        },
        {
            "desc": "Add course to manager",
            "func": "add_course",
            "setup": lambda: student_module.CourseManager(),
            "call": lambda obj: (obj.add_course("PY101", "Python Basics", 2), obj.courses.get("PY101")),
            "check": lambda result: isinstance(result, tuple) and result[1] == {"title": "Python Basics", "max": 2, "students": []},
            "marks": 5
        },
        {
            "desc": "Register student to course",
            "func": "register_student",
            "setup": lambda: _setup_register(student_module),
            "call": lambda obj: (obj.register_student("PY101", "Bob"), obj.courses["PY101"]["students"]),
            "check": lambda result: isinstance(result, tuple) and "Enrolled in Python Basics" in result[0] and "Bob" in result[1],
            "marks": 5
        },
        {
            "desc": "Get available seats in course",
            "func": "get_available_seats",
            "setup": lambda: _setup_seats(student_module),
            "call": lambda obj: obj.get_available_seats("PY101"),
            "check": lambda result: result == 1,
            "marks": 5
        },
        {
            "desc": "Remove student from course",
            "func": "remove_student",
            "setup": lambda: _setup_remove(student_module),
            "call": lambda obj: (obj.remove_student("PY101", "Bob"), "Bob" in obj.courses["PY101"]["students"]),
            "check": lambda result: isinstance(result, tuple) and "Removed Bob from Python Basics" in result[0] and result[1] == False,
            "marks": 5
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 5)
        
        max_score += marks
        
        try:
            obj = case["setup"]()
            
            # Execute test
            result = case["call"](obj)
            passed = case["check"](result)
            
            if passed:
                msg = f"PASS Visible Test Case {idx} Passed: {case['desc']}"
                total_score += marks
            else:
                msg = f"FAIL Visible Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"
            
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL Visible Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"
            print(msg)
            report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/25.0 (Visible)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


def _setup_register(student_module):
    """Setup for register student test."""
    manager = student_module.CourseManager()
    manager.add_course("PY101", "Python Basics", 2)
    return manager


def _setup_seats(student_module):
    """Setup for available seats test."""
    manager = student_module.CourseManager()
    manager.add_course("PY101", "Python Basics", 2)
    manager.register_student("PY101", "Bob")
    return manager


def _setup_remove(student_module):
    """Setup for remove student test."""
    manager = student_module.CourseManager()
    manager.add_course("PY101", "Python Basics", 2)
    manager.register_student("PY101", "Bob")
    return manager


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
