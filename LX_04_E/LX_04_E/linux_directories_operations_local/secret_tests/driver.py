import json
import os
import sys
import socket
from datetime import datetime, timezone, timedelta

HOME = os.path.expanduser('~')

START_TIME_STR = os.getenv('KODEBUCK_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', 'LOCAL_USER')

def verify_task():
    print("\n" + "-" * 60)
    print(f"{'KODEBUCK LOCAL LINUX DIRECTORY OPERATIONS VERIFICATION':^60}")
    print(f"System Hostname: {socket.gethostname()}")
    print("-" * 60)

    total_score = 0
    results = {}
    
    def check_mtime(path):
        if not START_TIME:
            return True
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
            return mtime >= START_TIME - timedelta(minutes=5)
        except Exception:
            return False

    home_dirs = ['/home/ubuntu', '/home/LabsKraft', HOME]
    active_home = HOME
    for d in home_dirs:
        if os.path.isdir(d):
            if os.path.isdir(os.path.join(d, 'workspace')) or os.path.isfile(os.path.join(d, 'final.txt')):
                active_home = d
                break

    # TC1: Environment active and verified
    tc1_passed = os.path.exists(active_home) and os.path.isdir(active_home)
    results['tc1'] = tc1_passed
    total_score += 0
    print(f"TC1: {'Local VM Environment active':<30} [{'PASSED' if tc1_passed else 'FAILED'}] (0/0)")

    # TC2: Directory 'workspace' and file 'temp.txt' created successfully
    tc2_passed = False
    if tc1_passed:
        target_dir = os.path.join(active_home, 'workspace')
        target_file = os.path.join(target_dir, 'temp.txt')
        final_file = os.path.join(active_home, 'final.txt')
        if os.path.isdir(target_dir) and (os.path.isfile(target_file) or os.path.isfile(final_file)):
            if check_mtime(target_dir) or check_mtime(target_file) or check_mtime(final_file):
                tc2_passed = True
    results['tc2'] = tc2_passed
    total_score += 5 if tc2_passed else 0
    print(f"TC2: {'workspace/temp.txt created':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({5 if tc2_passed else 0}/5)")

    # TC3: File moved and renamed to '/home/ubuntu/final.txt' successfully
    tc3_passed = False
    if tc1_passed:
        final_file = os.path.join(active_home, 'final.txt')
        if os.path.isfile(final_file):
            if check_mtime(final_file):
                tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 5 if tc3_passed else 0
    print(f"TC3: {'temp.txt moved and renamed to final.txt':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({5 if tc3_passed else 0}/5)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/10")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    
    sol_path = os.path.join(ws_path, 'solution.json')
    existing_data = {}
    if os.path.exists(sol_path):
        try:
            with open(sol_path, 'r') as f:
                existing_data = json.load(f)
        except Exception:
            pass

    existing_data.update({'score': total_score, 'results': results})

    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump(existing_data, f, indent=4)
    with open(os.path.join(ws_path, 'solution.py'), 'w') as f:
        json.dump(existing_data, f, indent=4)
        
    root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
        json.dump(existing_data, f, indent=4)
    with open(os.path.join(root_ws_path, 'solution.py'), 'w') as f:
        json.dump(existing_data, f, indent=4)

if __name__ == "__main__":
    verify_task()
