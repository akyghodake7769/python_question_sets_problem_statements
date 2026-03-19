import pandas as pd
import os
import sys
import importlib.util

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
    # Output path setup
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    # Load solution
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}")
        return
    
    print("Running Tests for: Patient Health Monitor (Dynamic Anti-Cheat Mode)\n")
    report_lines = ["Running Tests for: Patient Health Monitor (Dynamic Anti-Cheat Mode)\n"]
    
    if not hasattr(solution, "HealthMonitor"):
        print("ERROR: HealthMonitor class not found")
        return
    
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

    # Execute tests with dynamic modifications
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
                # Modify: Add 3 extra NaN rows
                extra = pd.DataFrame({'PatientID':['X','Y','Z'], 'Day':['Mon']*3, 'HeartRate':[None]*3})
                test_df = pd.concat([raw_df, extra], ignore_index=True)
                temp.df = test_df.copy()
                actual = temp.clean_records()
                expected = test_df['HeartRate'].isna().sum()
            elif idx == 4:
                desc = "Find Highest Rate (Logic)"
                marks = 4
                # Modify: Inject a peak rate of 160
                test_df = cleaned_df.copy()
                test_df.iloc[0, test_df.columns.get_loc('HeartRate')] = 160
                temp.df = test_df.copy()
                actual = temp.find_highest_rate()
                expected = 160
            elif idx == 5:
                desc = "Patient Averages (Logic)"
                marks = 4
                # Modify: Fix P01 values to all be 90
                test_df = cleaned_df.copy()
                test_df.loc[test_df['PatientID'] == 'P01', 'HeartRate'] = 90
                temp.df = test_df.copy()
                res = temp.patient_averages()
                actual = res.get('P01') if isinstance(res, dict) else res
                expected = 90.0
            elif idx == 6:
                desc = "High Risk Identification (Logic)"
                marks = 4
                # Modify: Add a very high risk patient
                test_df = cleaned_df.copy()
                test_df.loc[0, 'PatientID'] = 'P_HIGH'
                test_df.loc[0, 'HeartRate'] = 150
                temp.df = test_df.copy()
                actual = temp.high_risk(140)
                expected = ['P_HIGH']
            elif idx == 7:
                desc = "Count High Risk Patients (Logic)"
                marks = 4
                # Modify: 3 patients high risk
                test_df = cleaned_df.copy()
                test_df.loc[0:2, 'HeartRate'] = 140
                temp.df = test_df.copy()
                temp.high_risk = lambda t: ['P01','P02','P03'] if t == 135 else []
                actual = temp.count_high_risk(135)
                expected = 3

            if actual == expected:
                if marks > 0:
                    total_score += marks
                    msg = f"PASS TC{idx} [{desc}] (4/4)"
                else:
                    msg = f"PASS TC{idx} [{desc}] (Sample)"
            else:
                msg = f"FAIL TC{idx} [{desc}] | Expected: {expected}, Got: {actual}"
            
        except Exception as e:
            msg = f"FAIL TC{idx} | Error: {str(e)}"
        
        print(msg)
        report_lines.append(msg)

    print(f"\nSCORE: {total_score}/{max_score}")
    report_lines.append(f"\nSCORE: {total_score}/{max_score}")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
