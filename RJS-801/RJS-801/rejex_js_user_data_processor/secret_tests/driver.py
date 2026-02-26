import importlib.util
import os
import sys

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found in class. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable. Make sure it's defined as a method."
    return True, None

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    # Clear previous report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("")

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(student_module)
    except SyntaxError as e:
        error_msg = f"SYNTAX ERROR: {str(e)}"
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return

    print("Running Tests for: User Data Processor\n")
    report_lines = ["Running Tests for: User Data Processor\n"]

    # Verify class exists
    if not hasattr(student_module, "UserDataProcessor"):
        error_msg = "ERROR: UserDataProcessor class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return

    test_cases = [
        {
            "desc": "Initialize UserDataProcessor",
            "func": "initialize",
            "setup": lambda: student_module.UserDataProcessor(),
            "call": lambda obj: (isinstance(obj.users, list), len(obj.users)),
            "check": lambda result: result[0] and result[1] == 0,
            "expected_output": "Empty users list initialized",
            "marks": 5
        },
        {
            "desc": "Validate email addresses",
            "func": "validate_email",
            "setup": lambda: student_module.UserDataProcessor(),
            "call": lambda obj: (obj.validate_email("user@example.com"), obj.validate_email("invalid-email")),
            "check": lambda result: result[0] is True and result[1] is False,
            "expected_output": "Valid email returns True, invalid email returns False",
            "marks": 5
        },
        {
            "desc": "Validate phone numbers",
            "func": "validate_phone",
            "setup": lambda: _setup_processor(student_module),
            "call": lambda obj: (obj.validate_phone("+1-234-567-8900"), obj.validate_phone("123")),
            "check": lambda result: result[0] is True and result[1] is False,
            "expected_output": "Valid phone returns True, invalid phone returns False",
            "marks": 5
        },
        {
            "desc": "Extract usernames from text",
            "func": "extract_usernames",
            "setup": lambda: _setup_processor(student_module),
            "call": lambda obj: sorted(obj.extract_usernames("Hello @john and @jane")),
            "check": lambda result: result == ['jane', 'john'],
            "expected_output": "Extracted usernames: ['jane', 'john']",
            "marks": 5
        },
        {
            "desc": "Mask sensitive data",
            "func": "mask_sensitive_data",
            "setup": lambda: _setup_processor(student_module),
            "call": lambda obj: (obj.mask_sensitive_data("Contact: user@example.com", "email"), obj.mask_sensitive_data("Call: 234-567-8900", "phone")),
            "check": lambda result: "***@***" in result[0] and "***-***-****" in result[1],
            "expected_output": "Email and phone masked in text",
            "marks": 5
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 5)
        max_score += marks
        
        try:
            # Verify method exists (skip for initialization test)
            if case["func"] != "initialize":
                method_exists, error_msg = validate_method_exists(student_module.UserDataProcessor(), case["func"])
                if not method_exists:
                    msg = f"FAIL TC{idx} [{case['desc']}]: {error_msg}"
                    print(msg)
                    report_lines.append(msg)
                    continue
            
            # Setup and execute test
            obj = case["setup"]()
            result = case["call"](obj)
            passed = case["check"](result)
            
            if passed:
                msg = f"PASS TC{idx} [{case['desc']}]"
                total_score += marks
            else:
                msg = f"FAIL TC{idx} [{case['desc']}]\n"
                msg += f"  Expected: {case['expected_output']}\n"
                msg += f"  Got: {repr(result)}"
            
            print(msg)
            report_lines.append(msg)
        
        except TypeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Type Mismatch Error\n"
            msg += f"  Details: {str(e)}"
            print(msg)
            report_lines.append(msg)
        
        except ValueError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Value Error\n"
            msg += f"  Details: {str(e)}"
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: {type(e).__name__}\n"
            msg += f"  Details: {str(e)}"
            print(msg)
            report_lines.append(msg)

    # ============ FINAL SCORING ============
    score_line = f"\nSCORE: {total_score}/{max_score} (Visible)"
    
    if total_score == 0:
        score_line += "\n⚠️ No tests passed. Make sure to implement all required methods."
    
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


def _setup_processor(student_module):
    """Setup for validation tests."""
    processor = student_module.UserDataProcessor()
    return processor


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
