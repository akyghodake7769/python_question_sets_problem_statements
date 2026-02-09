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
    problem_code = "hotel_booking_performance_analysis_pandas"
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
        analyzer = student_module.HotelBookingAnalyzer()
        results.append("✓ solution.py loaded")
    except Exception as e:
        results.append(f"✗ Failed to load HotelBookingAnalyzer: {e}")
        _write_report(report_file, results)
        return

    results.append(f"\n🧪 Running Tests for: Hotel Booking Performance Analysis\n")

    # Define test DataFrames
    test_df_1 = pd.DataFrame({
        "Guest": ["Alice", "Bob"],
        "Hotel": ["Hotel Blue", "Hotel Red"],
        "Date": ["2024-06-01", "2024-06-02"],
        "Status": ["Booked", "Cancelled"],
        "Amount": [300.0, 0.0]
    })

    test_df_2 = pd.DataFrame({
        "Guest": ["Alice", "Alice", "Bob"],
        "Hotel": ["Hotel Blue", "Hotel Blue", "Hotel Red"],
        "Date": ["2024-06-01", "2024-06-15", "2024-06-02"],
        "Status": ["Booked", "Booked", "Booked"],
        "Amount": [300.0, 250.0, 400.0]
    })

    test_df_3 = pd.DataFrame({
        "Guest": ["Alice", "Bob", "Zoe"],
        "Hotel": ["Hotel Blue", "Hotel Red", "Hotel Green"],
        "Date": ["2024-06-01", "2024-06-02", "2024-06-03"],
        "Status": ["Booked", "Cancelled", "No-show"],
        "Amount": [300.0, 200.0, 150.0]
    })

    test_df_4 = pd.DataFrame({
        "Guest": ["Alice", "Bob", "Alice", "Bob", "Zoe"],
        "Hotel": ["Hotel Blue", "Hotel Red", "Hotel Blue", "Hotel Red", "Hotel Green"],
        "Date": ["2024-06-01", "2024-06-02", "2024-06-05", "2024-06-06", "2024-06-07"],
        "Status": ["Booked", "No-show", "Cancelled", "No-show", "Booked"],
        "Amount": [300.0, 200.0, 250.0, 180.0, 150.0]
    })

    # Hidden test DataFrames
    test_df_invalid = pd.DataFrame({
        "Guest": ["Alice", "Bob", "Zoe", "Tom"],
        "Hotel": ["Hotel Blue", "Hotel Red", "Hotel Green", "Hotel Gold"],
        "Date": ["2024-06-01", "2024-06-02", "2024-06-03", "2024-06-04"],
        "Status": ["Booked", "Invalid", "Cancelled", "Pending"],
        "Amount": [300.0, 200.0, -50.0, None]
    })

    test_df_only_booked = pd.DataFrame({
        "Guest": ["Alice", "Alice", "Bob"],
        "Hotel": ["Hotel Blue", "Hotel Blue", "Hotel Red"],
        "Date": ["2024-07-01", "2024-07-15", "2024-07-02"],
        "Status": ["Booked", "Booked", "Booked"],
        "Amount": [300.0, 250.0, 400.0]
    })

    test_df_one_status = pd.DataFrame({
        "Guest": ["Alice", "Bob", "Zoe"],
        "Hotel": ["Hotel Blue", "Hotel Blue", "Hotel Red"],
        "Date": ["2024-06-01", "2024-06-02", "2024-06-03"],
        "Status": ["Booked", "Booked", "Booked"],
        "Amount": [300.0, 200.0, 150.0]
    })

    test_cases = [
        {
            "desc": "Create structured booking DataFrame",
            "func": "create_booking_df",
            "input": [["Alice", "Hotel Blue", "2024-06-01", "Booked", 300.0]],
            "expected_type": pd.DataFrame,
            "marks": 2.5
        },
        {
            "desc": "Compute monthly revenue per hotel",
            "func": "compute_monthly_revenue",
            "input": test_df_2.copy(),
            "expected_columns": ["Hotel", "Month", "Revenue"],
            "marks": 2.5
        },
        {
            "desc": "Add cancellation flag column",
            "func": "add_cancellation_flag",
            "input": test_df_1.copy(),
            "expected_columns": ["IsCancelled"],
            "marks": 2.5
        },
        {
            "desc": "Identify guests with frequent no-shows",
            "func": "get_no_show_guests",
            "input": (test_df_4.copy(), 0),
            "expected_columns": ["Guest", "NoShowCount"],
            "marks": 2.5
        },
        {
            "desc": "Hotel-wise status summary",
            "func": "hotel_status_summary",
            "input": test_df_3.copy(),
            "expected_columns": ["Hotel"],
            "marks": 2.5
        },
        {
            "desc": "Clean records with null/invalid status",
            "func": "clean_booking_data",
            "input": test_df_invalid.copy(),
            "expected_rows": 2,
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Handle guests with only booked stays",
            "func": "compute_monthly_revenue",
            "input": test_df_only_booked.copy(),
            "expected_columns": ["Hotel", "Month", "Revenue"],
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Hotel with only one type of status",
            "func": "hotel_status_summary",
            "input": test_df_one_status.copy(),
            "expected_columns": ["Hotel"],
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
                msg = f"❌ Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
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
                msg = f"✅ {test_type} Test Case {idx} Passed: {case['desc']}"
                total_score += marks
                if is_hidden:
                    hidden_score += marks
                else:
                    visible_score += marks
            else:
                test_type = "Hidden" if is_hidden else "Visible"
                msg = f"❌ {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"

        except Exception as e:
            test_type = "Hidden" if is_hidden else "Visible"
            msg = f"❌ {test_type} Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"

        results.append(msg)

    # Final score report
    results.append(f"\n🎯 SCORE: {visible_score}/12.5 (Visible) + {hidden_score}/7.5 (Hidden) = {total_score}/20 (Total)")

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
