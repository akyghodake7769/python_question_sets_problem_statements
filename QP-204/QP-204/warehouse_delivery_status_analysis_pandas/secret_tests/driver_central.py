import importlib.util
import os
import datetime
import pytz
from pathlib import Path
import pandas as pd
import inspect

IST = pytz.timezone("Asia/Kolkata")

def get_timestamp():
    return datetime.datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")

def test_student_code(solution_path, vm_tag):
    problem_code = "warehouse_delivery_status_analysis_pandas"
    base_dir = Path("/home/ubuntu/central_server")
    report_base_dir = base_dir / "reports" / problem_code / vm_tag
    os.makedirs(report_base_dir, exist_ok=True)

    timestamp = get_timestamp()
    report_file = report_base_dir / f"{vm_tag}_{timestamp}.txt"

    results = [f">> Testing solution for {vm_tag} at {timestamp}"]

    # Load student solution
    try:
        spec = importlib.util.spec_from_file_location("student_solution", solution_path)
        student_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student_module)
        analyzer = student_module.DeliveryAnalyzer()
        results.append("solution.py loaded")
    except Exception as e:
        results.append(f"Failed to load DeliveryAnalyzer: {e}")
        _write_report(report_file, results)
        return

    results.append(f"\nRunning Tests for: Warehouse Delivery Status Analysis\n")

    # Define test DataFrames
    test_df_1 = pd.DataFrame({
        "DeliveryID": [1001, 1002],
        "Warehouse": ["WH1", "WH2"],
        "Date": ["2024-06-01", "2024-06-01"],
        "Status": ["Delivered", "Delayed"]
    })

    test_df_2 = pd.DataFrame({
        "DeliveryID": [1001, 1002, 1003],
        "Warehouse": ["WH1", "WH1", "WH2"],
        "Date": ["2024-06-01", "2024-06-02", "2024-06-01"],
        "Status": ["Delivered", "Returned", "Delayed"]
    })

    test_df_3 = pd.DataFrame({
        "DeliveryID": [1001, 1002],
        "Warehouse": ["WH1", "WH2"],
        "Date": ["2024-06-01", "2024-06-01"],
        "Status": ["Delivered", "Delayed"]
    })

    test_df_4 = pd.DataFrame({
        "DeliveryID": [1001, 1002, 1003],
        "Warehouse": ["WH1", "WH1", "WH2"],
        "Date": ["2024-06-01", "2024-06-02", "2024-06-03"],
        "Status": ["Returned", "Returned", "Delivered"]
    })

    test_df_5 = pd.DataFrame({
        "DeliveryID": [1001, 1002, 1003],
        "Warehouse": ["WH1", "WH2", "WH1"],
        "Date": ["2024-06-01", "2024-06-01", "2024-06-02"],
        "Status": ["Delivered", "Delayed", "Returned"]
    })

    # Hidden test DataFrames
    test_df_invalid = pd.DataFrame({
        "DeliveryID": [1001, 1002, 1003],
        "Warehouse": ["WH1", "WH2", "WH1"],
        "Date": ["2024-06-01", "2024-06-01", "2024-06-02"],
        "Status": ["Delivered", "Lost", None]
    })

    test_df_perfect = pd.DataFrame({
        "DeliveryID": [1001, 1002],
        "Warehouse": ["WH3", "WH3"],
        "Date": ["2024-06-01", "2024-06-02"],
        "Status": ["Delivered", "Delivered"]
    })

    test_df_single_status = pd.DataFrame({
        "DeliveryID": [1001, 1002],
        "Warehouse": ["WH4", "WH4"],
        "Date": ["2024-06-01", "2024-06-02"],
        "Status": ["Returned", "Returned"]
    })

    test_cases = [
        {
            "desc": "Create structured delivery DataFrame",
            "func": "create_delivery_df",
            "input": [[1001, "WH1", "2024-06-01", "Delivered"]],
            "expected_type": pd.DataFrame,
            "marks": 2.5
        },
        {
            "desc": "Compute monthly delivery rate per warehouse",
            "func": "compute_monthly_delivery_rate",
            "input": test_df_2.copy(),
            "expected_columns": ["Warehouse", "Month", "Delivery Rate"],
            "marks": 2.5
        },
        {
            "desc": "Add delay flag column",
            "func": "add_delay_flag",
            "input": test_df_3.copy(),
            "expected_columns": ["IsDelayed"],
            "marks": 2.5
        },
        {
            "desc": "Identify warehouses with frequent returns",
            "func": "high_returns",
            "input": (test_df_4.copy(), 1),
            "expected_columns": ["Warehouse", "Return Count"],
            "marks": 2.5
        },
        {
            "desc": "Warehouse-wise status summary",
            "func": "warehouse_status_summary",
            "input": test_df_5.copy(),
            "expected_columns": ["Warehouse"],
            "marks": 2.5
        },
        {
            "desc": "Clean records with invalid status and nulls",
            "func": "clean_delivery_data",
            "input": test_df_invalid.copy(),
            "expected_rows": 1,
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Handle warehouse with perfect delivery rate",
            "func": "compute_monthly_delivery_rate",
            "input": test_df_perfect.copy(),
            "expected_columns": ["Warehouse", "Month", "Delivery Rate"],
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Warehouse with only one type of status",
            "func": "warehouse_status_summary",
            "input": test_df_single_status.copy(),
            "expected_columns": ["Warehouse"],
            "marks": 2.5,
            "is_hidden": True
        }
    ]

    total_score = 0
    max_score = 0
    visible_score = 0
    visible_max = 0
    hidden_score = 0
    hidden_max = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 2.5)
        is_hidden = case.get("is_hidden", False)
        max_score += marks
        
        if is_hidden:
            hidden_max += marks
        else:
            visible_max += marks
        
        try:
            func = getattr(analyzer, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()

            if 'pass' in src and len(src) < 80:
                msg = f"FAIL Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                results.append(msg)
                continue

            if isinstance(case["input"], tuple):
                result = func(*case["input"])
            elif isinstance(case["input"], list):
                result = func(case["input"])
            else:
                result = func(case["input"])

            passed = False
            if "expected_type" in case:
                passed = isinstance(result, case["expected_type"])
            elif "expected_columns" in case:
                passed = all(col in result.columns for col in case["expected_columns"])
            elif "expected_rows" in case:
                passed = result.shape[0] == case["expected_rows"]

            if passed:
                test_type = "Hidden" if is_hidden else "Visible"
                msg = f"PASS {test_type} Test Case {idx} Passed: {case['desc']}"
                total_score += marks
                if is_hidden:
                    hidden_score += marks
                else:
                    visible_score += marks
            else:
                test_type = "Hidden" if is_hidden else "Visible"
                msg = f"FAIL {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"

        except Exception as e:
            test_type = "Hidden" if is_hidden else "Visible"
            msg = f"FAIL {test_type} Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"

        results.append(msg)

    # Final score report
    results.append(f"\nSCORE: {visible_score}/12.5 (Visible) + {hidden_score}/7.5 (Hidden) = {total_score}/20 (Total)")

    _write_report(report_file, results)

def _write_report(report_file, lines):
    with open(report_file, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python driver_central.py <vm_tag> [solution_path]")
        sys.exit(1)
    
    vm_tag = sys.argv[1]
    solution_path = sys.argv[2] if len(sys.argv) > 2 else "/home/ubuntu/submissions/solution.py"
    test_student_code(solution_path, vm_tag)
