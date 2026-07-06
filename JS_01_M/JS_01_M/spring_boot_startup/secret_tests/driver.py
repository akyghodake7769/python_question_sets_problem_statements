import json
import os
import subprocess
import urllib.request
import urllib.error
import socket
import re

def get_base_path():
    # Attempt to get the workspace directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    base_path = get_base_path()
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False,
        "tc4": False,
        "tc5": False
    }

    # TC1: Compile codebase
    try:
        process = subprocess.run(
            ['mvn', 'clean', 'compile'],
            cwd=base_path,
            capture_output=True,
            text=True
        )
        if process.returncode == 0:
            results['tc1'] = True
    except Exception:
        pass

    # TC2: Check for Stereotype annotation in UserService
    try:
        user_service_path = os.path.join(base_path, 'src/main/java/com/kloudlabs/app/service/UserService.java')
        with open(user_service_path, 'r') as f:
            content = f.read()
            if '@Service' in content or '@Component' in content:
                results['tc2'] = True
    except Exception:
        pass

    # TC3: Check application.properties for port 8081
    try:
        props_path = os.path.join(base_path, 'src/main/resources/application.properties')
        with open(props_path, 'r') as f:
            content = f.read()
            if re.search(r'server\.port\s*=\s*8081', content):
                results['tc3'] = True
    except Exception:
        pass

    # TC4: Check if application is listening on port 8081
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('127.0.0.1', 8081))
        if result == 0:
            results['tc4'] = True
        sock.close()
    except Exception:
        pass

    # TC5: Check actuator health endpoint
    try:
        req = urllib.request.Request('http://localhost:8081/actuator/health')
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                if data.get('status') == 'UP':
                    results['tc5'] = True
    except Exception:
        pass

    return results

if __name__ == "__main__":
    test_results = run_tests()
    print(json.dumps(test_results))
