from datetime import datetime, timezone, timedelta
import os
import sys
import importlib.util
import random
import copy
import re

# Global IST offset for consistent reporting
ist_offset = timezone(timedelta(hours=5, minutes=30))

def get_timestamp():
    """Returns timestamp in YYYYMMDD_HHMMSS format (IST assumption)"""
    return datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")

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

def test_student_code(solution_path, vm_tag="DEFAULT"):
    problem_code = "cardiac_vitals_dictionary_analyzer"
    
    if vm_tag is None:
        vm_tag = "DEFAULT"
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

    results = [f">> Testing solution for {username} at {timestamp}"]
    report_items = []
    total_score = 0
    fail_count = 0
    
    try:
        spec = importlib.util.spec_from_file_location("solution", solution_path)
        solution = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(solution)
        HealthMonitor = solution.HealthMonitor
    except Exception as e:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"IMPORT ERROR: {e}\n")
        print(f"IMPORT ERROR: {e}")
        return

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
    
    total_tc = len(tc_configs)
    print(f"Running Evaluation for: {problem_code}\n")
    print(f"{'Test Case':<15} | {'Status':<10} | {'Marks'}")
    print("-" * 50)
    
    random.seed(None)
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
                        o2 = "health_cardiac.csv available"
                    else:
                        p_ok = False
                        exp2 = "health_cardiac.csv available"
                        o2 = "health_cardiac.csv missing or failed to load"
                elif i == 2:
                    # Validate successful data loading
                    if csv_loaded_ok:
                        try:
                            obj = HealthMonitor()
                            obj.read_data(health_csv)
                            if obj.records is not None and len(obj.records) == loaded_records_count:
                                p_ok = True
                                exp2 = f"Loaded {loaded_records_count} records"
                                o2 = f"Loaded {len(obj.records)} records"
                            else:
                                p_ok = False
                                exp2 = f"Loaded {loaded_records_count} records"
                                o2 = f"Loaded {len(obj.records) if obj.records is not None else 0} records"
                        except Exception as e:
                            p_ok = False
                            exp2 = f"Loaded {loaded_records_count} records"
                            o2 = f"Error: {e}"
                    else:
                        p_ok = False
                        exp2 = "records loaded successfully (> 0)"
                        o2 = "no records loaded (CSV missing)"
            else:
                rv = random.randint(115, 150)
                
                # Setup obj1 (base run)
                obj1 = HealthMonitor()
                if i == 3:
                    o1 = run_t(i, obj1, raw_records)
                else:
                    o1 = run_t(i, obj1, cleaned_records)
                
                # Setup obj2 (dynamic run)
                obj2 = HealthMonitor()
                if i == 3:
                    # In dyn_raw, we make one more record None
                    dyn_raw = copy.deepcopy(raw_records)
                    for k, v in dyn_raw.items():
                        if v['HeartRate'] is not None:
                            v['HeartRate'] = None
                            break
                    o2 = run_t(i, obj2, dyn_raw)
                    initial_none_count = sum(1 for v in raw_records.values() if v['HeartRate'] is None)
                    exp2 = initial_none_count + 1
                else:
                    dyn_records = copy.deepcopy(cleaned_records)
                    for k, v in dyn_records.items():
                        if v['PatientID'] == 'P01':
                            v['HeartRate'] = rv
                            break
                    o2 = run_t(i, obj2, dyn_records)
                    
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
                
                if o2 == exp2:
                    p_ok = True
                elif o2 is None:
                    none_ret = True
                elif o1 == o2:
                    h_det = True

            tc_name = f"TC{i} [{desc}]"
            report_items.append(tc_name)
            
            if p_ok:
                total_score += marks
                status = "PASSED"
                results.append(f"✓ {tc_name}: PASSED ({marks if marks > 0 else 'Sample'})")
            else:
                status = "FAILED"
                fail_count += 1
                if none_ret:
                    reason = "Method not implemented / No return value"
                elif h_det:
                    reason = "Hardcoded. Dynamic check failed."
                else:
                    reason = f"Incorrect Output. Expected: {exp2} | Actual: {o2}"
                results.append(f"✗ {tc_name}: FAILED (0/{marks}) | {reason}")
                
            print(f"TC{i:02d} [{desc[:30]:<30}] | {status:<10} | {marks if status == 'PASSED' else 0}/{marks}")

        except Exception as e:
            status = "FAILED"
            fail_count += 1
            results.append(f"✗ TC{i} [{desc}]: FAILED (0/{marks}) | Error: {e}")
            print(f"TC{i:02d} [{desc[:30]:<30}] | {status:<10} | 0/{marks}")

    print("-" * 50)
    print(f"{'TOTAL SCORE':<15} | {'':<10} | {total_score}/20")
    results.append(f"\n🎯 TOTAL SCORE: {total_score}/20")

    # Write report file if on server
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(results) + "\n")
    except Exception:
        pass

    # Final Standardized CSV Output (8-Column Format)
    date_str = datetime.now(ist_offset).strftime("%d-%m-%Y")
    csv_report = f"{date_str},{problem_code},{username},{timestamp},{total_tc}: {'; '.join(report_items)},,{fail_count},{total_score}"
    print(f"\n[REPORT_CSV]: {csv_report}")

if __name__ == "__main__":
    vm = sys.argv[1] if len(sys.argv) > 1 else "DEFAULT"
    sol = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol, vm)
