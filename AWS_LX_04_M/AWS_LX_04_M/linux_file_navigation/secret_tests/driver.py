import json
import os
import sys
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
    
    # TC1: Environment active and verified
    tc1_passed = os.path.exists('/home/ubuntu') and os.path.isdir('/home/ubuntu')
    results['tc1'] = tc1_passed
    total_score += 4 if tc1_passed else 0
    print(f"TC1: {'Local VM Environment active':<30} [{'PASSED' if tc1_passed else 'FAILED'}] ({4 if tc1_passed else 0}/4)")

    # TC2: Directory hierarchy created
    tc2_passed = False
    if tc1_passed:
        if os.path.isdir('/home/ubuntu/app/config') and os.path.isdir('/home/ubuntu/app/logs'):
            tc2_passed = True
    results['tc2'] = tc2_passed
    total_score += 4 if tc2_passed else 0
    print(f"TC2: {'Directory hierarchy created':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({4 if tc2_passed else 0}/4)")

    # TC3: Initial files created
    tc3_passed = False
    if tc1_passed:
        if os.path.isfile('/home/ubuntu/app/config/app.conf') and os.path.isfile('/home/ubuntu/app/logs/error.log'):
            tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 4 if tc3_passed else 0
    print(f"TC3: {'Initial files created':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({4 if tc3_passed else 0}/4)")

    # TC4: File operations completed
    tc4_passed = False
    if tc1_passed:
        if os.path.isfile('/home/ubuntu/app/app.conf.backup') and os.path.isfile('/home/ubuntu/search_results.txt'):
            tc4_passed = True
    results['tc4'] = tc4_passed
    total_score += 4 if tc4_passed else 0
    print(f"TC4: {'File operations completed':<30} [{'PASSED' if tc4_passed else 'FAILED'}] ({4 if tc4_passed else 0}/4)")

    # TC5: Disk usage output generated
    tc5_passed = False
    if tc1_passed:
        if os.path.isfile('/home/ubuntu/disk_usage.txt') and os.path.getsize('/home/ubuntu/disk_usage.txt') > 0:
            tc5_passed = True
    results['tc5'] = tc5_passed
    total_score += 4 if tc5_passed else 0
    print(f"TC5: {'Disk usage output generated':<30} [{'PASSED' if tc5_passed else 'FAILED'}] ({4 if tc5_passed else 0}/4)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/20")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump({'score': total_score, 'results': results}, f, indent=4)

if __name__ == "__main__":
    verify_task()
