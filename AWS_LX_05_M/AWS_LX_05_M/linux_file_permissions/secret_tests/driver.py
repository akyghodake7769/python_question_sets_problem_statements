import json
import os
import sys
import pwd
from datetime import datetime, timezone, timedelta

START_TIME_STR = os.getenv('KODEBUCK_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', 'LOCAL_USER')

def verify_task():
    print("\n" + "-" * 60)
    print(f"{'KODEBUCK LOCAL LINUX VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}
    
    # TC1: User appuser created successfully
    tc1_passed = False
    try:
        pwd.getpwnam('appuser')
        tc1_passed = True
    except KeyError:
        pass
    results['tc1'] = tc1_passed
    total_score += 5 if tc1_passed else 0
    print(f"TC1: {'User appuser created':<30} [{'PASSED' if tc1_passed else 'FAILED'}] ({5 if tc1_passed else 0}/5)")

    # TC2: Files and directory created
    tc2_passed = os.path.isdir('/home/ubuntu/secure_data') and os.path.isfile('/home/ubuntu/secure_data/passwords.txt') and os.path.isfile('/home/ubuntu/secure_data/config.ini')
    results['tc2'] = tc2_passed
    total_score += 5 if tc2_passed else 0
    print(f"TC2: {'Files and directory created':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({5 if tc2_passed else 0}/5)")

    # TC3: Proper permissions applied
    tc3_passed = False
    if os.path.isfile('/home/ubuntu/secure_data/passwords.txt') and os.path.isfile('/home/ubuntu/secure_data/config.ini'):
        p_mode = oct(os.stat('/home/ubuntu/secure_data/passwords.txt').st_mode & 0o777)
        c_mode = oct(os.stat('/home/ubuntu/secure_data/config.ini').st_mode & 0o777)
        if p_mode == '0o400' and c_mode == '0o755':
            tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 5 if tc3_passed else 0
    print(f"TC3: {'Proper permissions applied':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({5 if tc3_passed else 0}/5)")

    # TC4: Ownership configured correctly
    tc4_passed = False
    if os.path.isfile('/home/ubuntu/secure_data/config.ini'):
        try:
            owner = pwd.getpwuid(os.stat('/home/ubuntu/secure_data/config.ini').st_uid).pw_name
            if owner == 'appuser':
                tc4_passed = True
        except KeyError:
            pass
    results['tc4'] = tc4_passed
    total_score += 5 if tc4_passed else 0
    print(f"TC4: {'Ownership configured correctly':<30} [{'PASSED' if tc4_passed else 'FAILED'}] ({5 if tc4_passed else 0}/5)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/20")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump({'score': total_score, 'results': results}, f, indent=4)

if __name__ == "__main__":
    verify_task()
