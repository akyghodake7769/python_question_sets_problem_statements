import importlib.util
import os
import inspect
import numpy as np

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "traffic_logs.csv")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    print("Running Tests for: Server Traffic Logs Analysis\n")
    report_lines = ["Running Tests for: Server Traffic Logs Analysis\n"]

    test_cases = [
        {
            "desc": "Load traffic_logs.csv and verify 20 rows loaded",
            "func": "read_logs",
            "setup": lambda: (lambda obj: (obj.read_logs(data_dir), obj)[-1])(student_module.TrafficAnalyzer()),
            "call": lambda obj: len(obj.df),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 20,
            "marks": 2
        },
        {
            "desc": "Identify and remove 2 outliers (ResponseTime > 10s)",
            "func": "sanitize_latency",
            "setup": lambda: (lambda obj: (obj.read_logs(data_dir), obj)[-1])(student_module.TrafficAnalyzer()),
            "call": lambda obj: obj.sanitize_latency(),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 2,
            "marks": 3
        },
        {
            "desc": "Verify 18 rows remain after outlier removal",
            "func": "sanitize_latency",
            "setup": lambda: (lambda obj: (obj.read_logs(data_dir), obj.sanitize_latency(), obj)[-1])(student_module.TrafficAnalyzer()),
            "call": lambda obj: len(obj.df),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 18,
            "marks": 2
        },
        {
            "desc": "Fill NaN values in ResponseTime with mean",
            "func": "fix_missing_records",
            "setup": lambda: (lambda obj: (obj.read_logs(data_dir), obj.fix_missing_records(), obj)[-1])(student_module.TrafficAnalyzer()),
            "call": lambda obj: obj.df['ResponseTime'].isna().sum(),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 0,
            "marks": 3
        },
        {
            "desc": "Identify slowest endpoint (/profile with ~0.93s avg)",
            "func": "get_slowest_endpoint",
            "setup": lambda: (lambda obj: (obj.read_logs(data_dir), obj.sanitize_latency(), obj.fix_missing_records(), obj)[-1])(student_module.TrafficAnalyzer()),
            "call": lambda obj: obj.get_slowest_endpoint(),
            "check": lambda result: isinstance(result, str) and result == "/profile",
            "marks": 3
        },
        {
            "desc": "Count 404 errors in traffic logs",
            "func": "count_errors",
            "setup": lambda: (lambda obj: (obj.read_logs(data_dir), obj)[-1])(student_module.TrafficAnalyzer()),
            "call": lambda obj: obj.count_errors(404),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 2,
            "marks": 3
        },
        {
            "desc": "Check for 500 errors (should return 0)",
            "func": "count_errors",
            "setup": lambda: (lambda obj: (obj.read_logs(data_dir), obj)[-1])(student_module.TrafficAnalyzer()),
            "call": lambda obj: obj.count_errors(500),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 0,
            "marks": 2
        },
        {
            "desc": "Verify row count is correct after all operations",
            "func": "fix_missing_records",
            "setup": lambda: (lambda obj: (obj.read_logs(data_dir), obj.sanitize_latency(), obj.fix_missing_records(), obj)[-1])(student_module.TrafficAnalyzer()),
            "call": lambda obj: len(obj.df),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 18,
            "marks": 2
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 2)
        is_hidden = case.get("is_hidden", False)
        
        if not is_hidden:
            max_score += marks
        
        try:
            obj = case["setup"]()
            
            # Check for pass-only implementation
            func = getattr(obj, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()
            if 'pass' in src and len(src) < 80:
                test_type = "Hidden" if is_hidden else "Visible"
                msg = f"FAIL {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                report_lines.append(msg)
                print(msg)
                continue
            
            # Execute test
            result = case["call"](obj)
            passed = case["check"](result)
            
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
