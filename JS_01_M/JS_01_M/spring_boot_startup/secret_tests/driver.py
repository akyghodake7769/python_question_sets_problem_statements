import json
import os
import sys
import subprocess
import urllib.request
import urllib.error
import socket
import re
from datetime import datetime, timezone, timedelta

START_TIME_STR = os.getenv('KODEBUCK_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', 'LOCAL_USER')


def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))


def verify_task():
    print("\n" + "-" * 60)
    print(f"{'KODEBUCK JAVA SPRING BOOT VERIFICATION':^60}")
    print("-" * 60)

    base_path = get_base_path()
    total_score = 0
    results = {}

    # TC1: Compile codebase using Maven
    tc1_passed = False
    try:
        process = subprocess.run(
            ['mvn', 'clean', 'compile', '-q'],
            cwd=base_path,
            capture_output=True,
            text=True,
            timeout=120
        )
        if process.returncode == 0:
            tc1_passed = True
    except Exception:
        pass
    results['tc1'] = tc1_passed
    total_score += 4 if tc1_passed else 0
    print(f"TC1: {'Maven compile successful':<30} [{'PASSED' if tc1_passed else 'FAILED'}] ({4 if tc1_passed else 0}/4)")

    # TC2: Check for @Service or @Component stereotype annotation in UserService
    tc2_passed = False
    try:
        user_service_path = os.path.join(base_path, 'src/main/java/com/kloudlabs/app/service/UserService.java')
        with open(user_service_path, 'r') as f:
            content = f.read()
            if '@Service' in content or '@Component' in content:
                tc2_passed = True
    except Exception:
        pass
    results['tc2'] = tc2_passed
    total_score += 4 if tc2_passed else 0
    print(f"TC2: {'Spring @Service annotation added':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({4 if tc2_passed else 0}/4)")

    # TC3: Check application.properties for port 8081
    tc3_passed = False
    try:
        props_path = os.path.join(base_path, 'src/main/resources/application.properties')
        with open(props_path, 'r') as f:
            content = f.read()
            if re.search(r'server\.port\s*=\s*8081', content):
                tc3_passed = True
    except Exception:
        pass
    results['tc3'] = tc3_passed
    total_score += 4 if tc3_passed else 0
    print(f"TC3: {'Port configured to 8081':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({4 if tc3_passed else 0}/4)")

    # TC4: Check if application is listening on port 8081
    tc4_passed = False
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('127.0.0.1', 8081))
        if result == 0:
            tc4_passed = True
        sock.close()
    except Exception:
        pass
    results['tc4'] = tc4_passed
    total_score += 4 if tc4_passed else 0
    print(f"TC4: {'App running on port 8081':<30} [{'PASSED' if tc4_passed else 'FAILED'}] ({4 if tc4_passed else 0}/4)")

    # TC5: Check actuator health endpoint returns { "status": "UP" }
    tc5_passed = False
    try:
        req = urllib.request.Request('http://localhost:8081/actuator/health')
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                if data.get('status') == 'UP':
                    tc5_passed = True
    except Exception:
        pass
    results['tc5'] = tc5_passed
    total_score += 4 if tc5_passed else 0
    print(f"TC5: {'Actuator health endpoint UP':<30} [{'PASSED' if tc5_passed else 'FAILED'}] ({4 if tc5_passed else 0}/4)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/20")
    print("-" * 60 + "\n")

    # Save results to solution.json and solution.py (KodeBuck IDE reads solution.py)
    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)

    output_data = {'score': total_score, 'results': results}

    # Load any existing metadata (e.g. assessment_start_time, candidate_prefix)
    sol_json_path = os.path.join(ws_path, 'solution.json')
    try:
        if os.path.isfile(sol_json_path):
            with open(sol_json_path, 'r') as f:
                metadata = json.load(f)
                metadata.update(output_data)
                output_data = metadata
    except Exception:
        pass

    with open(sol_json_path, 'w') as f:
        json.dump(output_data, f, indent=4)
    # KodeBuck IDE is hardcoded to upload solution.py
    with open(os.path.join(ws_path, 'solution.py'), 'w') as f:
        json.dump(output_data, f, indent=4)

    # Also save at the parent root level (spring_boot_startup/)
    root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
        json.dump(output_data, f, indent=4)
    with open(os.path.join(root_ws_path, 'solution.py'), 'w') as f:
        json.dump(output_data, f, indent=4)


if __name__ == "__main__":
    verify_task()
