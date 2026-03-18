import pandas as pd
import os
import sys
import importlib.util

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}")
        return
    
    print("Running Tests for: Patient Health Monitor (7 Methods | 5 Marked)\n")
    report_lines = ["Running Tests for: Patient Health Monitor (7 Methods | 5 Marked)\n"]
    
    if not hasattr(solution, "HealthMonitor"):
        print("ERROR: HealthMonitor class not found")
        return
    
    HealthMonitor = solution.HealthMonitor
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    health_csv = os.path.join(data_dir, 'health.csv')
    
    # Data for independence
    raw_df = pd.read_csv(health_csv)
    cleaned_df = raw_df.dropna().copy()
    
    test_cases = [
        {"desc": "clean_records - Removed Count", "func": "clean_records", "marks": 4},
        {"desc": "clean_records - Final State", "func": "clean_records_state", "marks": 4},
        {"desc": "find_highest_rate", "func": "find_highest_rate", "marks": 4},
        {"desc": "patient_averages", "func": "patient_averages", "marks": 4},
        {"desc": "high_risk", "func": "high_risk", "marks": 4}
    ]

    total_score = 0
    max_score = 20.0

    for idx, case in enumerate(test_cases, 1):
        try:
            temp = HealthMonitor()
            # Foundation methods are assumed pre-filled correctly as they are 0-marks
            temp.df = None
            temp.read_data(health_csv)
            
            # Map logical checks
            actual = None
            expected = None
            
            if idx == 1: # clean_records result
                temp.df = raw_df.copy()
                actual = temp.clean_records()
                expected = 2
            elif idx == 2: # clean_records state
                temp.df = raw_df.copy()
                temp.clean_records()
                actual = len(temp.df) if temp.df is not None else 0
                expected = 10
            elif idx == 3: # find_highest_rate
                temp.df = cleaned_df.copy()
                actual = temp.find_highest_rate()
                expected = 110
            elif idx == 4: # patient_averages
                temp.df = cleaned_df.copy()
                res_dict = temp.patient_averages()
                actual = round(res_dict.get('P01', 0), 2) if isinstance(res_dict, dict) else res_dict
                expected = 72.33
            elif idx == 5: # high_risk
                temp.df = cleaned_df.copy()
                actual = temp.high_risk(100)
                expected = ['P03']
            
            if actual == expected:
                msg = f"PASS TC{idx} [{case['desc']}] (4/4)"
                total_score += 4
            else:
                msg = f"FAIL TC{idx} [{case['desc']}] | Expected: {expected}, Got: {actual}"
            
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}] | Error: {str(e)}"
        
        print(msg)
        report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/{max_score}"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
