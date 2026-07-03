import json
import os
import sys
from datetime import datetime, timezone, timedelta

START_TIME_STR = os.getenv('KODEBUCK_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', 'LOCAL_USER')

def verify_task():
    print("\n" + "-" * 60)
    print(f"{'KODEBUCK LOCAL LINUX MONITORING VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}
    
    # TC1: CPU/process logs generated
    tc1_passed = os.path.isfile('/home/ubuntu/cpu_monitor.txt') and os.path.getsize('/home/ubuntu/cpu_monitor.txt') > 0
    results['tc1'] = tc1_passed
    total_score += 5 if tc1_passed else 0
    print(f"TC1: {'CPU/process logs generated':<30} [{'PASSED' if tc1_passed else 'FAILED'}] ({5 if tc1_passed else 0}/5)")

    # TC2: Memory logs generated
    tc2_passed = os.path.isfile('/home/ubuntu/memory.txt') and os.path.getsize('/home/ubuntu/memory.txt') > 0
    results['tc2'] = tc2_passed
    total_score += 5 if tc2_passed else 0
    print(f"TC2: {'Memory logs generated':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({5 if tc2_passed else 0}/5)")

    # TC3: Disk logs generated
    tc3_passed = os.path.isfile('/home/ubuntu/disk.txt') and os.path.getsize('/home/ubuntu/disk.txt') > 0
    results['tc3'] = tc3_passed
    total_score += 5 if tc3_passed else 0
    print(f"TC3: {'Disk logs generated':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({5 if tc3_passed else 0}/5)")

    # TC4: Network logs generated
    tc4_passed = os.path.isfile('/home/ubuntu/network.txt') and os.path.getsize('/home/ubuntu/network.txt') > 0
    results['tc4'] = tc4_passed
    total_score += 5 if tc4_passed else 0
    print(f"TC4: {'Network logs generated':<30} [{'PASSED' if tc4_passed else 'FAILED'}] ({5 if tc4_passed else 0}/5)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/20")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump({'score': total_score, 'results': results}, f, indent=4)

if __name__ == "__main__":
    verify_task()
