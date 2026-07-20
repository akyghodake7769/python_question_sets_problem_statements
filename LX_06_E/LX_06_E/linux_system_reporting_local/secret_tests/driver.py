import json
import os
import sys
from datetime import datetime, timezone, timedelta

HOME = '/home/LabsKraft' if os.path.isdir('/home/LabsKraft') else os.path.expanduser('~')

START_TIME_STR = os.getenv('KODEBUCK_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', 'LOCAL_USER')

def check_mtime(path):
    if not START_TIME:
        return True
    try:
        mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
        return mtime >= START_TIME - timedelta(minutes=5)
    except Exception:
        return False

def verify_task():
    print("\n" + "-" * 60)
    print(f"{'KODEBUCK LOCAL LINUX SYSTEM REPORTING VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}

    # TC1: Environment active and verified
    tc1_passed = os.path.exists(HOME) and os.path.isdir(HOME)
    results['tc1'] = tc1_passed
    total_score += 0
    print(f"TC1: {'Local VM Environment active':<30} [{'PASSED' if tc1_passed else 'FAILED'}] (0/0)")

    # TC2: spec_report.txt contains system specs
    tc2_passed = False
    if tc1_passed:
        target_file = os.path.join(HOME, 'spec_report.txt')
        if os.path.isfile(target_file) and os.path.getsize(target_file) > 0:
            if check_mtime(target_file):
                try:
                    with open(target_file, 'r') as f:
                        content = f.read().lower()
                        if 'disk' in content or 'mem' in content or 'used' in content or 'filesystem' in content:
                            tc2_passed = True
                except Exception:
                    tc2_passed = True
    results['tc2'] = tc2_passed
    total_score += 5 if tc2_passed else 0
    print(f"TC2: {'spec_report.txt created':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({5 if tc2_passed else 0}/5)")

    # TC3: search_results.txt contains log search
    tc3_passed = False
    if tc1_passed:
        target_file = os.path.join(HOME, 'search_results.txt')
        if os.path.isfile(target_file) and os.path.getsize(target_file) > 0:
            if check_mtime(target_file):
                try:
                    with open(target_file, 'r') as f:
                        content = f.read().lower()
                        if 'nameserver' in content or '127.0.0.1' in content or 'dns' in content or len(content) > 0:
                            tc3_passed = True
                except Exception:
                    tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 5 if tc3_passed else 0
    print(f"TC3: {'search_results.txt created':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({5 if tc3_passed else 0}/5)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/10")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    
    output_data = {'score': total_score, 'results': results}
    
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump(output_data, f, indent=4)
    with open(os.path.join(ws_path, 'solution.py'), 'w') as f:
        json.dump(output_data, f, indent=4)
        
    root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
        json.dump(output_data, f, indent=4)
    with open(os.path.join(root_ws_path, 'solution.py'), 'w') as f:
        json.dump(output_data, f, indent=4)

if __name__ == "__main__":
    verify_task()
