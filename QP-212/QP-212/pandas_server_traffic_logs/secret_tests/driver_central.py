import importlib.util
import os
import sys
from datetime import datetime, timezone, timedelta
import inspect
import numpy as np
import re

# Global IST offset for consistent reporting
ist_offset = timezone(timedelta(hours=5, minutes=30))

def get_timestamp():
    """Returns timestamp in YYYYMMDD_HHMMSS format (IST assumption)"""
    return datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")

def test_student_code(solution_path, vm_tag="DEFAULT"):
    problem_code = "pandas_server_traffic_logs"
    
    # Extract username and timestamp from vm_tag if it's in the server structure
    match = re.search(r'TRIAL_([^_]+)_(\d{8}_\d{6})', vm_tag)
    if match:
        username, timestamp = match.groups()
    else:
        username = vm_tag
        timestamp = get_timestamp()

    # Reporting setup for central server
    report_base = f"/home/ubuntu/central_server/reports/{problem_code}/{username}"
    os.makedirs(report_base, exist_ok=True)
    report_path = os.path.join(report_base, f"{username}_{timestamp}.txt")
    
    # Fallback for local testing
    if not os.path.exists("/home/ubuntu/central_server"):
        report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, f"{username}_{timestamp}.txt")

    data_dir = "/home/ubuntu/central_server/data/traffic_logs.csv"
    if not os.path.exists(data_dir):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "traffic_logs.csv")

    results = [f">> Testing solution for {username} at {timestamp}"]
    report_items = []

    try:
        spec = importlib.util.spec_from_file_location("student_solution", solution_path)
        student_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student_module)
    except Exception as e:
        error_msg = f"IMPORT ERROR: Failed to load TrafficAnalyzer: {e}"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        print(error_msg)
        return

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
        },
        {
            "desc": "Verify count_errors returns 0 for non-existent code",
            "func": "count_errors",
            "setup": lambda: (lambda obj: (obj.read_logs(data_dir), obj)[-1])(student_module.TrafficAnalyzer()),
            "call": lambda obj: obj.count_errors(999),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 0,
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Verify sanitize_latency removes exact outliers",
            "func": "sanitize_latency",
            "setup": lambda: (lambda obj: (obj.read_logs(data_dir), obj.sanitize_latency(), obj)[-1])(student_module.TrafficAnalyzer()),
            "call": lambda obj: (obj.df['ResponseTime'] > 10.0).sum(),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 0,
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Verify fix_missing_records fills with correct mean",
            "func": "fix_missing_records",
            "setup": lambda: (lambda obj: (obj.read_logs(data_dir), obj.fix_missing_records(), obj)[-1])(student_module.TrafficAnalyzer()),
            "call": lambda obj: obj.df['ResponseTime'].isna().sum(),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 0,
            "marks": 2.5,
            "is_hidden": True
        }
    ]

    total_score = 0
    fail_count = 0
    total_tc = len(test_cases)
    
    print(f"Running Evaluation for: {problem_code}\n")
    print(f"{'Test Case':<15} | {'Status':<10} | {'Marks'}")
    print("-" * 55)

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 2)
        is_hidden = case.get("is_hidden", False)
        tc_type = "Hidden" if is_hidden else "Visible"
        tc_name = f"TC{idx} [{case['desc']}]"
        report_items.append(f"TC{idx} ({tc_type})")
        
        try:
            obj = case["setup"]()
            func = getattr(obj, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()
            
            if 'pass' in src and len(src) < 80:
                status = "FAILED"
                fail_count += 1
                msg = f"✗ {tc_name}: FAILED (0/{marks}) | Reason: Contains only 'pass'"
            else:
                result = case["call"](obj)
                passed = case["check"](result)
                if passed:
                    status = "PASSED"
                    total_score += marks
                    msg = f"✓ {tc_name}: PASSED ({marks})"
                else:
                    status = "FAILED"
                    fail_count += 1
                    msg = f"✗ {tc_name}: FAILED (0/{marks}) | Reason: Output mismatch"
            
            results.append(msg)
            print(f"TC{idx:02d} [{case['desc'][:30]:<30}] | {status:<10} | {marks if status == 'PASSED' else 0}/{marks}")
        
        except Exception as e:
            status = "FAILED"
            fail_count += 1
            msg = f"✗ {tc_name}: FAILED (0/{marks}) | Error: {str(e)}"
            results.append(msg)
            print(f"TC{idx:02d} [{case['desc'][:30]:<30}] | {status:<10} | 0/{marks}")

    print("-" * 55)
    print(f"{'TOTAL SCORE':<15} | {'':<10} | {total_score}/27.5")
    results.append(f"\n🎯 TOTAL SCORE: {total_score}/27.5")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results) + "\n")

    # Final Standardized CSV Output (8-Column Format)
    date_str = datetime.now(ist_offset).strftime("%d-%m-%Y")
    csv_report = f"{date_str},{problem_code},{username},{timestamp},{total_tc}: {'; '.join(report_items)},,{fail_count},{total_score}"
    print(f"\n[REPORT_CSV]: {csv_report}")


if __name__ == "__main__":
    vm = sys.argv[1] if len(sys.argv) > 1 else "DEFAULT"
    sol = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol, vm)
