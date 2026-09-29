import json
import os
import sys
import tarfile
from datetime import datetime, timezone, timedelta
import socket

def get_home():
    for p in ['/home/LabsKraft', '/home/ubuntu', '/home/labskraft']:
        if os.path.isdir(p):
            return p
    return os.path.expanduser('~')

HOME = get_home()

START_TIME_STR = os.getenv('KODEBUCK_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', 'LOCAL_USER')

def get_aws_metadata():
    import urllib.request
    try:
        token_req = urllib.request.Request("http://169.254.169.254/latest/api/token", headers={'X-aws-ec2-metadata-token-ttl-seconds': '21600'}, method='PUT')
        token = urllib.request.urlopen(token_req, timeout=1).read().decode()
        id_req = urllib.request.Request("http://169.254.169.254/latest/meta-data/instance-id", headers={'X-aws-ec2-metadata-token': token})
        instance_id = urllib.request.urlopen(id_req, timeout=1).read().decode()
        region_req = urllib.request.Request("http://169.254.169.254/latest/meta-data/placement/region", headers={'X-aws-ec2-metadata-token': token})
        region = urllib.request.urlopen(region_req, timeout=1).read().decode()
        return instance_id, region
    except Exception:
        return None, None

def find_file(filename):
    candidates = [
        os.path.join(HOME, filename),
        os.path.join('/home/ubuntu', filename),
        os.path.join('/home/LabsKraft', filename),
        os.path.join('/home/labskraft', filename),
        os.path.join(os.path.expanduser('~'), filename)
    ]
    seen = set()
    for c in candidates:
        if c not in seen and (os.path.isfile(c) or os.path.isdir(c)):
            return c
        seen.add(c)
    return os.path.join(HOME, filename)

def verify_task():
    print("\n" + "-" * 60)
    print(f"{'KODEBUCK LOCAL LINUX VERIFICATION':^60}")
    print(f"System Hostname: {socket.gethostname()}")
    print("-" * 60)

    total_score = 0
    results = {}

    def check_mtime(path):
        if not START_TIME:
            return True
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
            return mtime >= START_TIME - timedelta(minutes=15)
        except Exception:
            return True

    # TC1: Local VM Environment active and verified
    tc1_passed = os.path.exists(HOME) and os.path.isdir(HOME)
    results['tc1'] = tc1_passed
    print(f"TC1: {'VM Environment Verification':<30} [{'PASSED' if tc1_passed else 'FAILED'}] (0/0)")

    # TC2: Network Connectivity (ping_results.txt)
    tc2_passed = False
    ping_file = find_file('ping_results.txt')
    if os.path.isfile(ping_file) and check_mtime(ping_file):
        try:
            with open(ping_file, 'r') as f:
                content = f.read().lower()
                if ("ping statistics" in content or "bytes from" in content) and "100% packet loss" not in content:
                    tc2_passed = True
        except Exception:
            pass
    results['tc2'] = tc2_passed
    total_score += 4 if tc2_passed else 0
    print(f"TC2: {'Network Connectivity Log':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({4 if tc2_passed else 0}/4)")

    # TC3: Port Diagnostics (open_ports.txt)
    tc3_passed = False
    ports_file = find_file('open_ports.txt')
    if os.path.isfile(ports_file) and check_mtime(ports_file):
        try:
            with open(ports_file, 'r') as f:
                content = f.read()
                if any(k in content for k in ["State", "Local Address", "Proto", "LISTEN", "udp", "tcp"]) or len(content.strip()) > 30:
                    tc3_passed = True
        except Exception:
            pass
    results['tc3'] = tc3_passed
    total_score += 4 if tc3_passed else 0
    print(f"TC3: {'Port Diagnostics Report':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({4 if tc3_passed else 0}/4)")

    # TC4: IP Configuration (ip_config.txt)
    tc4_passed = False
    ip_file = find_file('ip_config.txt')
    if os.path.isfile(ip_file) and check_mtime(ip_file):
        try:
            with open(ip_file, 'r') as f:
                content = f.read()
                if any(k in content for k in ["inet ", "ether ", "lo:", "eth0:", "ens", "link/"]):
                    tc4_passed = True
        except Exception:
            pass
    results['tc4'] = tc4_passed
    total_score += 4 if tc4_passed else 0
    print(f"TC4: {'IP Configuration Report':<30} [{'PASSED' if tc4_passed else 'FAILED'}] ({4 if tc4_passed else 0}/4)")

    # TC5: Dummy log file creation
    tc5_passed = False
    log_file = find_file('dummy_app.log')
    if os.path.isfile(log_file) and check_mtime(log_file):
        tc5_passed = True
    results['tc5'] = tc5_passed
    total_score += 4 if tc5_passed else 0
    print(f"TC5: {'Dummy Log File Creation':<30} [{'PASSED' if tc5_passed else 'FAILED'}] ({4 if tc5_passed else 0}/4)")

    # TC6: File Compression (app_archive.tar.gz contains dummy_app.log)
    tc6_passed = False
    archive_file = find_file('app_archive.tar.gz')
    if os.path.isfile(archive_file) and check_mtime(archive_file):
        try:
            with tarfile.open(archive_file, 'r:gz') as tar:
                names = tar.getnames()
                if any("dummy_app.log" in name for name in names):
                    tc6_passed = True
        except Exception:
            pass
    results['tc6'] = tc6_passed
    total_score += 4 if tc6_passed else 0
    print(f"TC6: {'Tarball Archive Compression':<30} [{'PASSED' if tc6_passed else 'FAILED'}] ({4 if tc6_passed else 0}/4)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/20")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    sol_path = os.path.join(ws_path, 'solution.json')
    existing_data = {}
    if os.path.exists(sol_path):
        try:
            with open(sol_path, 'r') as f:
                existing_data = json.load(f)
        except Exception: pass
    
    output_data = dict(existing_data)
    output_data.update({'score': total_score, 'results': results})
    instance_id, aws_region = get_aws_metadata()
    if instance_id:
        output_data['instance_id'] = instance_id
        output_data['aws_region'] = aws_region
    
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump(output_data, f, indent=4)
    with open(os.path.join(ws_path, 'solution.py'), 'w') as f:
        json.dump(output_data, f, indent=4)
        
    root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
        json.dump(output_data, f, indent=4)
    with open(os.path.join(root_ws_path, 'solution.py'), 'w') as f:
        json.dump(output_data, f, indent=4)

    extra_paths = []
    for base_h in [HOME, '/home/LabsKraft', '/home/ubuntu', '/home/labskraft']:
        extra_paths.extend([
            os.path.join(base_h, 'KodeBuck_Workspace', 'LX_03_M', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'LX_03_M', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'LX_03_M', 'student_workspace', 'solution.py'),
            os.path.join(base_h, 'KodeBuck_workspace', 'LX_03_M', 'student_workspace', 'solution.py'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'linux_monitoring_local', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'linux_monitoring_local', 'student_workspace', 'solution.json')
        ])
    for ep in extra_paths:
        try:
            os.makedirs(os.path.dirname(ep), exist_ok=True)
            with open(ep, 'w') as f:
                json.dump(output_data, f, indent=4)
        except Exception:
            pass

if __name__ == "__main__":
    verify_task()
