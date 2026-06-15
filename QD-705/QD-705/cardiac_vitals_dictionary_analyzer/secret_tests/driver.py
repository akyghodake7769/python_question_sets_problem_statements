import os
import sys
import importlib.util
import random
import copy

def resolve_health_csv_path():
    paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "health_cardiac.csv"),
        os.path.join(os.path.dirname(__file__), "health_cardiac.csv"),
        "/home/ubuntu/central_server/data/health_cardiac.csv",
        "secret_test/cardiac_vitals_dictionary_analyzer/data/health_cardiac.csv",
        "secret_test/cardiac_vitals_dictionary_analyzer/health_cardiac.csv",
        "secret_tests/cardiac_vitals_dictionary_analyzer/data/health_cardiac.csv",
        "secret_tests/cardiac_vitals_dictionary_analyzer/health_cardiac.csv"
    ]
    for p in paths:
        abs_p = os.path.abspath(p)
        if os.path.exists(abs_p): return abs_p
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
    
    # Fallback Base Data for Injection
    fallback_raw_records = {
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

    csv_loaded_ok = False
    loaded_records_count = 0
    raw_records = {}

    if health_csv is not None:
        try:
            import csv
            with open(health_csv, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for idx, row in enumerate(reader):
                    if len(row) < 3:
                        continue
                    patient_id, day, heart_rate = row[0], row[1], row[2]
                    hr_val = None
                    if heart_rate and heart_rate.strip():
                        try:
                            hr_val = int(heart_rate.strip())
                        except ValueError:
                            hr_val = None
                    raw_records[idx] = {
                        'PatientID': patient_id,
                        'Day': day,
                        'HeartRate': hr_val
                    }
            if len(raw_records) > 0:
                csv_loaded_ok = True
                loaded_records_count = len(raw_records)
        except Exception:
            csv_loaded_ok = False

    if not csv_loaded_ok:
        raw_records = copy.deepcopy(fallback_raw_records)

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
            if i <= 2:
                if i == 1:
                    # Validate CSV availability and loading
                    if csv_loaded_ok:
                        p_ok = True
                        exp2 = "health_cardiac.csv available"
                        res2 = "health_cardiac.csv available"
                    else:
                        p_ok = False
                        exp2 = "health_cardiac.csv available"
                        res2 = "health_cardiac.csv missing or failed to load"
                elif i == 2:
                    # Validate successful data loading
                    if csv_loaded_ok:
                        try:
                            obj = HealthMonitor()
                            obj.read_data(health_csv)
                            if obj.records is not None and len(obj.records) == loaded_records_count:
                                p_ok = True
                                exp2 = f"Loaded {loaded_records_count} records"
                                res2 = f"Loaded {len(obj.records)} records"
                            else:
                                p_ok = False
                                exp2 = f"Loaded {loaded_records_count} records"
                                res2 = f"Loaded {len(obj.records) if obj.records is not None else 0} records"
                        except Exception as e:
                            p_ok = False
                            exp2 = f"Loaded {loaded_records_count} records"
                            res2 = f"Error: {e}"
                    else:
                        p_ok = False
                        exp2 = "records loaded successfully (> 0)"
                        res2 = "no records loaded (CSV missing)"
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
                    initial_none_count = sum(1 for v in raw_records.values() if v['HeartRate'] is None)
                    exp2 = initial_none_count + 1
                else:
                    dyn_records = copy.deepcopy(cleaned_records)
                    for k, v in dyn_records.items():
                        if v['PatientID'] == 'P01':
                            v['HeartRate'] = rv
                            break
                    res2 = run_t(i, obj2, dyn_records)
                    
                    if i == 4:
                        exp2 = max(v['HeartRate'] for v in dyn_records.values())
                    elif i == 5:
                        expected_averages = {}
                        groups = {}
                        for v in dyn_records.values():
                            if v['HeartRate'] is not None:
                                groups.setdefault(v['PatientID'], []).append(v['HeartRate'])
                        for pid, rates in groups.items():
                            expected_averages[pid] = round(sum(rates) / len(rates), 2)
                        exp2 = expected_averages
                    elif i == 6:
                        high_risk_pts = set()
                        for v in dyn_records.values():
                            if v['HeartRate'] is not None and v['HeartRate'] > 100:
                                high_risk_pts.add(v['PatientID'])
                        exp2 = sorted(list(high_risk_pts))
                    elif i == 7:
                        high_risk_pts = set()
                        for v in dyn_records.values():
                            if v['HeartRate'] is not None and v['HeartRate'] > 100:
                                high_risk_pts.add(v['PatientID'])
                        exp2 = len(high_risk_pts)
                
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
