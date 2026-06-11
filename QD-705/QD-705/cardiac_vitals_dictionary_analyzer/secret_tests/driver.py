import os
import sys
import importlib.util
import random
import copy

def resolve_health_csv_path():
    paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "health.csv"),
        os.path.join(os.path.dirname(__file__), "health.csv")
    ]
    for p in paths:
        if os.path.exists(p): return p
    return None

def test_student_code(solution_path):
    report_dir = os.path.dirname(solution_path)
    report_path = os.path.join(report_dir, "report.txt")
    
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}")
        return
    
    print("Running Tests for: Cardiac Vitals Dictionary Analyzer\n")
    report_lines = ["Running Tests for: Cardiac Vitals Dictionary Analyzer\n"]
    
    if not hasattr(solution, "HealthMonitor"):
        print("ERROR: HealthMonitor class not found")
        return
    
    HealthMonitor = solution.HealthMonitor
    health_csv = resolve_health_csv_path()
    
    # Load base data for injection
    # In dictionary: records mapped by index
    raw_records = {
        0: {'PatientID': 'P01', 'Day': 'Mon', 'HeartRate': 72},
        1: {'PatientID': 'P02', 'Day': 'Mon', 'HeartRate': None},
        2: {'PatientID': 'P01', 'Day': 'Tue', 'HeartRate': 75},
        3: {'PatientID': 'P03', 'Day': 'Mon', 'HeartRate': 105},
        4: {'PatientID': 'P04', 'Day': 'Tue', 'HeartRate': 68},
        5: {'PatientID': 'P05', 'Day': 'Mon', 'HeartRate': 80},
        6: {'PatientID': 'P06', 'Day': 'Mon', 'HeartRate': None},
        7: {'PatientID': 'P01', 'Day': 'Wed', 'HeartRate': 70},
        8: {'PatientID': 'P03', 'Day': 'Tue', 'HeartRate': 110},
        9: {'PatientID': 'P04', 'Day': 'Wed', 'HeartRate': 75},
        10: {'PatientID': 'P02', 'Day': 'Tue', 'HeartRate': 85},
        11: {'PatientID': 'P05', 'Day': 'Wed', 'HeartRate': 90}
    }
    
    cleaned_records = {k: copy.deepcopy(v) for k, v in raw_records.items() if v['HeartRate'] is not None}

    tc_configs = [
        ("Initial State", 0),
        ("Data Loading", 0),
        ("Clean Records", 4),
        ("Find Highest Rate", 4),
        ("Patient Averages", 4),
        ("High Risk Identification", 4),
        ("Count High Risk Patients", 4)
    ]

    total_score = 0
    for i, (desc, marks) in enumerate(tc_configs, 1):
        try:
            def run_t(idx, current_obj, current_records=None):
                if idx == 1: 
                    return current_obj.records
                if idx == 2: 
                    current_obj.read_data(health_csv)
                    return len(current_obj.records) if current_obj.records is not None else 0
                if idx == 3: 
                    if current_records is not None:
                        current_obj.records = copy.deepcopy(current_records)
                    return current_obj.clean_records()
                if idx == 4: 
                    if current_records is not None:
                        current_obj.records = copy.deepcopy(current_records)
                    return current_obj.find_highest_rate()
                if idx == 5: 
                    if current_records is not None:
                        current_obj.records = copy.deepcopy(current_records)
                    res = current_obj.patient_averages()
                    return res
                if idx == 6: 
                    if current_records is not None:
                        current_obj.records = copy.deepcopy(current_records)
                    return current_obj.high_risk(100)
                if idx == 7: 
                    if current_records is not None:
                        current_obj.records = copy.deepcopy(current_records)
                    return current_obj.count_high_risk(100)
                return None

            p_ok, h_det, none_ret = False, False, False
            
            if i <= 2: # Samples
                res2 = run_t(i, HealthMonitor())
                exp2 = None if i == 1 else 12
                if i == 1:
                    p_ok = (res2 is None or res2 == {})
                else:
                    p_ok = (res2 == exp2)
            else:
                rv = random.randint(115, 150)
                
                # Setup obj1 (base run)
                obj1 = HealthMonitor()
                if i == 3:
                    res1 = run_t(i, obj1, raw_records)
                else:
                    res1 = run_t(i, obj1, cleaned_records)
                
                # Setup obj2 (dynamic run)
                obj2 = HealthMonitor()
                if i == 3:
                    # In dyn_raw, we make one more record None
                    dyn_raw = copy.deepcopy(raw_records)
                    for k, v in dyn_raw.items():
                        if v['HeartRate'] is not None:
                            v['HeartRate'] = None
                            break
                    res2 = run_t(i, obj2, dyn_raw)
                    exp2 = 3
                else:
                    dyn_records = copy.deepcopy(cleaned_records)
                    for k, v in dyn_records.items():
                        if v['PatientID'] == 'P01':
                            v['HeartRate'] = rv
                            break
                    res2 = run_t(i, obj2, dyn_records)
                    
                    if i == 4:
                        exp2 = rv
                    elif i == 5:
                        p01_vals = [v['HeartRate'] for v in dyn_records.values() if v['PatientID'] == 'P01' and v['HeartRate'] is not None]
                        exp2 = {
                            'P01': round(sum(p01_vals) / len(p01_vals), 2),
                            'P03': 107.5,
                            'P04': 71.5,
                            'P05': 85.0,
                            'P02': 85.0
                        }
                    elif i == 6:
                        exp2 = ['P01', 'P03']
                    elif i == 7:
                        exp2 = 2
                
                if res2 == exp2:
                    p_ok = True
                elif res2 is None:
                    none_ret = True
                elif res1 == res2:
                    h_det = True
            
            if p_ok:
                total_score += marks
                msg = f"PASS TC{i} [{desc}] ({marks if marks > 0 else 'Sample'})"
            elif none_ret:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Method not implemented / No return value"
            elif h_det:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Hardcoded. Dynamic check failed."
            else:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Incorrect Output. Expected: {exp2} | Actual: {res2}"
        except Exception as e:
            msg = f"FAIL TC{i} [{desc}] | Error: {e}"
        print(msg)
        report_lines.append(msg)

    print(f"\nSCORE: {total_score}/20.0")
    report_lines.append(f"\nSCORE: {total_score}/20.0")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")
