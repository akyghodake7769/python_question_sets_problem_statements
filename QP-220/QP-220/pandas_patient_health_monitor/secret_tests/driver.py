import pandas as pd
import os
import sys
import importlib.util
import random

def resolve_health_csv_path():
    """Resolve the path to health.csv. Priority: Local Relative > Data Dir."""
    paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "health.csv"),
        os.path.join(os.path.dirname(__file__), "health.csv")
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return
    
    print("Running Tests for: Patient Health Monitor (Randomized Anti-Cheat Mode)\n")
    report_lines = ["Running Tests for: Patient Health Monitor (Randomized Anti-Cheat Mode)\n"]
    
    if not hasattr(solution, "HealthMonitor"):
        print("ERROR: HealthMonitor class not found"); return
    
    HealthMonitor = solution.HealthMonitor
    health_csv = resolve_health_csv_path()
    if not health_csv:
        print("ERROR: health.csv not found"); return

    # Load base data
    try:
        raw_df = pd.read_csv(health_csv)
        cleaned_df = raw_df.dropna(subset=['HeartRate']).copy()
    except Exception as e:
        print(f"READ ERROR: {e}"); return

    total_score = 0
    max_score = 20.0

    # Randomized offsets for each run
    rand_nan = random.randint(3, 8)
    rand_peak = random.randint(130, 180)
    rand_p01_val = random.randint(75, 95)
    rand_risk_threshold = random.randint(110, 120)

    for idx in range(1, 8):
        try:
            temp = HealthMonitor()
            actual = None
            expected = None
            desc = ""
            marks = 0

            if idx == 1:
                desc = "Initial State (Sample)"
                actual = temp.df
                expected = None
            elif idx == 2:
                desc = "Data Loading (Sample)"
                temp.read_data(health_csv)
                actual = len(temp.df) if temp.df is not None else 0
                expected = 12
            elif idx == 3:
                desc = "Clean Records (Logic)"
                marks = 4
                # Add random number of NaN rows
                extra = pd.DataFrame({'PatientID':[f'X{i}' for i in range(rand_nan)], 'HeartRate':[None]*rand_nan})
                test_df = pd.concat([raw_df, extra], ignore_index=True)
                temp.df = test_df.copy()
                actual = temp.clean_records()
                expected = test_df['HeartRate'].isna().sum()
            elif idx == 4:
                desc = "Find Highest Rate (Logic)"
                marks = 4
                test_df = cleaned_df.copy()
                test_df.loc[0, 'HeartRate'] = rand_peak
                temp.df = test_df.copy()
                actual = temp.find_highest_rate()
                expected = rand_peak
            elif idx == 5:
                desc = "Patient Averages (Logic)"
                marks = 4
                test_df = cleaned_df.copy()
                test_df.loc[test_df['PatientID'] == 'P01', 'HeartRate'] = rand_p01_val
                temp.df = test_df.copy()
                res = temp.patient_averages()
                actual = res.get('P01') if isinstance(res, dict) else res
                expected = float(rand_p01_val)
            elif idx == 6:
                desc = "High Risk Identification (Logic)"
                marks = 4
                test_df = cleaned_df.copy()
                test_df.loc[0, 'PatientID'] = 'P_STRICT_RISK'
                test_df.loc[0, 'HeartRate'] = rand_risk_threshold + 5
                temp.df = test_df.copy()
                actual = temp.high_risk(rand_risk_threshold)
                expected = sorted(list(set(test_df[test_df['HeartRate'] > rand_risk_threshold]['PatientID'])))
            elif idx == 7:
                desc = "Count High Risk Patients (Logic)"
                marks = 4
                test_df = cleaned_df.copy()
                # Use a specific set of high risk patients for isolation
                temp.df = test_df.copy()
                temp.high_risk = lambda t: ['R1', 'R2', 'R3'] if t == 50 else []
                actual = temp.count_high_risk(50)
                expected = 3

            if actual == expected:
                if marks > 0: total_score += marks
                msg = f"PASS TC{idx} [{desc}]"
            else:
                msg = f"FAIL TC{idx} [{desc}] | Expected: {expected}, Got: {actual}"
            
        except Exception as e:
            msg = f"FAIL TC{idx} | Error: {str(e)}"
        
        print(msg); report_lines.append(msg)

    print(f"\nSCORE: {total_score}/{max_score}")
    report_lines.append(f"\nSCORE: {total_score}/{max_score}")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
