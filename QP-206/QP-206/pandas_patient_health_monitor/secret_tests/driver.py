import pandas as pd
import os
import sys
import importlib.util

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found in class. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable. Make sure it's defined as a method."
    return True, None

def test_student_code(solution_path):
    """Main test function that runs all test cases"""
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    # Clear previous report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("")

    # Load the student's solution
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(solution)
    except SyntaxError as e:
        error_msg = f"SYNTAX ERROR: {str(e)}\nFix the syntax error in solution.py before running tests."
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return
    except ImportError as e:
        error_msg = f"IMPORT ERROR: {str(e)}\nMake sure pandas is imported correctly in solution.py"
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return
    
    print("Running Tests for: Patient Health Monitor\n")
    report_lines = ["Running Tests for: Patient Health Monitor\n"]
    
    # Verify class exists
    if not hasattr(solution, "HealthMonitor"):
        error_msg = "ERROR: HealthMonitor class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return
    
    HealthMonitor = solution.HealthMonitor
    
    HealthMonitor = solution.HealthMonitor
    
    # Get the data path
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    health_csv = os.path.join(data_dir, 'health.csv')
    
    test_cases = [
        {
            "desc": "__init__ creates empty placeholder",
            "func": "initialize",  # Skip method check for init
            "setup": lambda: HealthMonitor(),
            "call": lambda obj: obj.df,
            "check": lambda result: result is None,
            "expected_output": "df attribute should be None initially",
            "marks": 2
        },
        {
            "desc": "Load health.csv and verify schema",
            "func": "read_data",
            "setup": lambda: HealthMonitor(),
            "call": lambda obj: (obj.read_data(health_csv), list(obj.df.columns)),
            "check": lambda result: result[1] == ['PatientID', 'Day', 'HeartRate'],
            "expected_output": "DataFrame should have columns: ['PatientID', 'Day', 'HeartRate']",
            "marks": 2
        },
        {
            "desc": "Drop NaN rows and return count",
            "func": "clean_records",
            "setup": lambda: _setup_clean_records(HealthMonitor, health_csv),
            "call": lambda obj: obj.clean_records(),
            "check": lambda result: isinstance(result, int) and result >= 0,
            "expected_output": "Should return integer count of removed rows (>= 0)",
            "marks": 4
        },
        {
            "desc": "Record count after cleaning matches",
            "func": "clean_records",
            "setup": lambda: _setup_count_test(HealthMonitor, health_csv),
            "call": lambda obj: _verify_count(obj),
            "check": lambda result: result['valid'],
            "expected_output": "Final count = Initial count - Removed count, Final > 0",
            "marks": 3
        },
        {
            "desc": "Mean heart rate per patient as dict",
            "func": "patient_averages",
            "setup": lambda: _setup_averages(HealthMonitor, health_csv),
            "call": lambda obj: obj.patient_averages(),
            "check": lambda result: isinstance(result, dict) and len(result) > 0 and all(isinstance(v, (int, float)) for v in result.values()),
            "expected_output": "Dictionary with PatientID keys and numeric mean HR values",
            "marks": 3
        },
        {
            "desc": "Patients with HR > 100 threshold",
            "func": "high_risk",
            "setup": lambda: _setup_high_risk(HealthMonitor, health_csv),
            "call": lambda obj: obj.high_risk(100),
            "check": lambda result: isinstance(result, list),
            "expected_output": "List of unique PatientID strings with at least one HR > 100",
            "marks": 3
        },
        {
            "desc": "Unique patient IDs with no duplicates",
            "func": "high_risk",
            "setup": lambda: _setup_unique(HealthMonitor, health_csv),
            "call": lambda obj: obj.high_risk(120),
            "check": lambda result: isinstance(result, list) and len(result) == len(set(result)) and result == sorted(result),
            "expected_output": "Sorted list with no duplicate patient IDs",
            "marks": 3
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 3)
        max_score += marks
        
        try:
            # Verify method exists (skip for initialization)
            if case["func"] != "initialize":
                method_exists, error_msg = validate_method_exists(HealthMonitor(), case["func"])
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
                msg = f"PASS TC{idx} [{case['desc']}] ({marks}/{marks})"
                total_score += marks
            else:
                # Provide detailed mismatch error
                msg = f"FAIL TC{idx} [{case['desc']}]\n"
                msg += f"  Expected: {case['expected_output']}\n"
                msg += f"  Got: {repr(result)}\n"
                msg += f"  Hint: Review the method implementation and data types"
            
            print(msg)
            report_lines.append(msg)
        
        except FileNotFoundError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: File Not Found\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Make sure health.csv exists in the data folder"
            print(msg)
            report_lines.append(msg)
        
        except AttributeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Attribute Not Found\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check the method implementation - ensure DataFrame operations are correct"
            print(msg)
            report_lines.append(msg)
        
        except TypeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Type Mismatch Error\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check method return types - clean_records() should return int, high_risk() should return list"
            print(msg)
            report_lines.append(msg)
        
        except ValueError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Value Error\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check your data processing logic"
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: {type(e).__name__}\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Review implementation for logic errors. Check method signatures match specification"
            print(msg)
            report_lines.append(msg)

    # ============ FINAL SCORING ============
    score_line = f"\nSCORE: {total_score}/{max_score} (Visible)"
    if total_score == 0:
        score_line += "\n⚠️ No tests passed. Make sure to implement all required methods with correct signatures."
    
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


def _setup_clean_records(HealthMonitor, health_csv):
    """Setup for clean_records test."""
    monitor = HealthMonitor()
    monitor.read_data(health_csv)
    return monitor


def _setup_count_test(HealthMonitor, health_csv):
    """Setup for count test."""
    monitor = HealthMonitor()
    monitor.read_data(health_csv)
    return monitor


def _verify_count(obj):
    """Verify that count after cleaning is correct."""
    initial_count = len(obj.df)
    removed_count = obj.clean_records()
    final_count = len(obj.df)
    
    # Check that math adds up correctly
    is_valid = (final_count == initial_count - removed_count) and (final_count > 0) and (removed_count >= 0)
    return {'valid': is_valid, 'initial': initial_count, 'removed': removed_count, 'final': final_count}


def _setup_averages(HealthMonitor, health_csv):
    """Setup for patient_averages test."""
    monitor = HealthMonitor()
    monitor.read_data(health_csv)
    monitor.clean_records()
    return monitor


def _setup_high_risk(HealthMonitor, health_csv):
    """Setup for high_risk test."""
    monitor = HealthMonitor()
    monitor.read_data(health_csv)
    monitor.clean_records()
    return monitor


def _setup_unique(HealthMonitor, health_csv):
    """Setup for unique ID test."""
    monitor = HealthMonitor()
    monitor.read_data(health_csv)
    monitor.clean_records()
    return monitor


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solution_path = sys.argv[1]
    else:
        solution_path = os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'solution.py')
    test_student_code(solution_path)
