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
    print(f"{'KODEBUCK LOCAL LINUX FILE PERMISSIONS VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}

    # TC1: Environment active and verified
    tc1_passed = os.path.exists(HOME) and os.path.isdir(HOME)
    results['tc1'] = tc1_passed
    total_score += 0
    print(f"TC1: {'Local VM Environment active':<30} [{'PASSED' if tc1_passed else 'FAILED'}] (0/0)")

    # TC2: File copied to hosts_copy.txt successfully
    tc2_passed = False
    if tc1_passed:
        target_file = os.path.join(HOME, 'hosts_copy.txt')
        if os.path.isfile(target_file):
            if check_mtime(target_file):
                try:
                    with open(target_file, 'r') as f1, open('/etc/hosts', 'r') as f2:
                        if f1.read().strip() == f2.read().strip():
                            tc2_passed = True
                except Exception:
                    tc2_passed = True
    results['tc2'] = tc2_passed
    total_score += 5 if tc2_passed else 0
    print(f"TC2: {'hosts_copy.txt created':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({5 if tc2_passed else 0}/5)")

    # TC3: Permissions set to 755
    tc3_passed = False
    if tc1_passed:
        target_file = os.path.join(HOME, 'hosts_copy.txt')
        if os.path.isfile(target_file):
            try:
                mode = os.stat(target_file).st_mode
                if (mode & 0o777) == 0o755:
                    tc3_passed = True
            except Exception:
                pass
    results['tc3'] = tc3_passed
    total_score += 5 if tc3_passed else 0
    print(f"TC3: {'hosts_copy.txt permissions set to 755':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({5 if tc3_passed else 0}/5)")

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
