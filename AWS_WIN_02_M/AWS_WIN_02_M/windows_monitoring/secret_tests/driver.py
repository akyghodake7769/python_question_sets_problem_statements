import json
import os
import sys
import subprocess
from datetime import datetime, timezone, timedelta

START_TIME_STR = os.getenv('KODEBUCK_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', 'LOCAL_USER')

def run_powershell(cmd):
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True,
            text=True,
            timeout=15
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception:
        return False, ""

def verify_task():
    print("\n" + "-" * 60)
    print(f"{'KODEBUCK LOCAL WINDOWS MONITORING VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}

    # TC1: Environment Verification
    tc1_passed = sys.platform == 'win32' or os.path.exists('C:\\Windows')
    results['tc1'] = tc1_passed
    total_score += 4 if tc1_passed else 0
    print(f"TC1: {'Local Windows Environment active':<30} [{'PASSED' if tc1_passed else 'FAILED'}] ({4 if tc1_passed else 0}/4)")

    # TC2: Service Management (IIS)
    tc2_passed = False
    if tc1_passed:
        cmd = "(Get-Service w3svc -ErrorAction SilentlyContinue).Status -eq 'Running'"
        success, output = run_powershell(cmd)
        if success and "True" in output:
            tc2_passed = True
    results['tc2'] = tc2_passed
    total_score += 4 if tc2_passed else 0
    print(f"TC2: {'Service Management (IIS)':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({4 if tc2_passed else 0}/4)")

    # TC3: Automated Monitoring (Scheduled Task)
    tc3_passed = False
    if tc1_passed:
        cmd = "[bool](Get-ScheduledTask -TaskName 'MemoryMonitorTask' -ErrorAction SilentlyContinue)"
        success, output = run_powershell(cmd)
        print(f"DEBUG TC3 -> success={success}, output={output!r}")
        if success and "True" in output:
            tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 4 if tc3_passed else 0
    print(f"TC3: {'Scheduled Task Configured':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({4 if tc3_passed else 0}/4)")

    # TC4: Disk and CPU Diagnostics
    tc4_passed = False
    if tc1_passed:
        check_files_cmd = "[bool](Test-Path 'C:\\workspace\\monitor\\disk_report.txt') -and [bool](Test-Path 'C:\\workspace\\monitor\\cpu_process_report.txt')"
        success, output = run_powershell(check_files_cmd)
        if success and "True" in output:
            read_disk = "Get-Content 'C:\\workspace\\monitor\\disk_report.txt' -Raw"
            d_success, d_output = run_powershell(read_disk)
            read_cpu = "Get-Content 'C:\\workspace\\monitor\\cpu_process_report.txt' -Raw"
            c_success, c_output = run_powershell(read_cpu)
            if d_success and c_success and len(d_output.strip()) > 0 and len(c_output.strip()) > 0:
                tc4_passed = True
    results['tc4'] = tc4_passed
    total_score += 4 if tc4_passed else 0
    print(f"TC4: {'Disk & CPU Diagnostics':<30} [{'PASSED' if tc4_passed else 'FAILED'}] ({4 if tc4_passed else 0}/4)")

    # TC5: Network & System Log Diagnostics
    tc5_passed = False
    if tc1_passed:
        check_files_cmd = "[bool](Test-Path 'C:\\workspace\\monitor\\network_status.txt') -and [bool](Test-Path 'C:\\workspace\\monitor\\event_errors.txt')"
        success, output = run_powershell(check_files_cmd)
        if success and "True" in output:
            read_net = "Get-Content 'C:\\workspace\\monitor\\network_status.txt' -Raw"
            n_success, n_output = run_powershell(read_net)
            read_err = "Get-Content 'C:\\workspace\\monitor\\event_errors.txt' -Raw"
            e_success, e_output = run_powershell(read_err)
            if n_success and e_success and len(n_output.strip()) > 0 and len(e_output.strip()) > 0:
                tc5_passed = True
    results['tc5'] = tc5_passed
    total_score += 4 if tc5_passed else 0
    print(f"TC5: {'Network & Log Diagnostics':<30} [{'PASSED' if tc5_passed else 'FAILED'}] ({4 if tc5_passed else 0}/4)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/20")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump({'score': total_score, 'results': results}, f, indent=4)

if __name__ == "__main__":
    verify_task()
