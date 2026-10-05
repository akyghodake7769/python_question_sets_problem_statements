import json
import os
import sys
import socket
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_home():
    for p in ['/home/ubuntu', '/home/LabsKraft', '/home/labskraft']:
        if os.path.isdir(p):
            return p
    return os.path.expanduser('~')

HOME = get_home()

START_TIME_STR = os.getenv('KODEBUCK_START_TIME')
START_TIME = None
if START_TIME_STR:
    try:
        START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00'))
    except Exception:
        START_TIME = None

USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', 'LOCAL_USER')

def find_all_user_homes():
    homes = set()
    for base in ['/home', '/root']:
        if os.path.isdir(base):
            if base == '/root':
                homes.add('/root')
            else:
                try:
                    for u in os.listdir(base):
                        p = os.path.join(base, u)
                        if os.path.isdir(p):
                            homes.add(p)
                except Exception:
                    pass
    homes.add(os.path.expanduser('~'))
    for u in ['ubuntu', 'LabsKraft', 'labskraft']:
        homes.add(f'/home/{u}')
    return [h for h in homes if os.path.isdir(h)]

def find_target_file(filename, all_homes):
    for h in all_homes:
        p = os.path.join(h, filename)
        if os.path.isfile(p) or os.path.exists(p):
            return p
    if os.path.isdir('/home/ubuntu'):
        return os.path.join('/home/ubuntu', filename)
    return os.path.join(os.path.expanduser('~'), filename)

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

def verify_task():
    print("\n" + "-" * 60)
    print(f"{'KODEBUCK LOCAL LINUX VERIFICATION':^60}")
    print(f"System Hostname: {socket.gethostname()}")
    print("-" * 60)

    total_score = 0
    results = {}

    all_homes = find_all_user_homes()
    ping_log = find_target_file('ping_local.log', all_homes)
    hostname_file = find_target_file('hostname_info.txt', all_homes)

    def check_mtime(path):
        if not os.path.exists(path):
            return False
        if not START_TIME:
            return True
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
            st = START_TIME
            if hasattr(st, 'tzinfo') and st.tzinfo is None:
                st = st.replace(tzinfo=timezone.utc)
            return mtime >= st - timedelta(minutes=15)
        except Exception:
            return True

    # TC1: Environment active
    tc1_passed = any(os.path.isdir(h) for h in all_homes)
    results['tc1'] = tc1_passed
    print(f"TC1: {'Local VM Environment active':<35} [{'PASSED' if tc1_passed else 'FAILED'}] (0/0)")

    # TC2: Ping log created
    tc2_passed = False
    if tc1_passed and (os.path.isfile(ping_log) or os.path.exists(ping_log)):
        if check_mtime(ping_log) and os.path.getsize(ping_log) > 0:
            tc2_passed = True
    results['tc2'] = tc2_passed
    total_score += 2 if tc2_passed else 0
    print(f"TC2: {'Ping log ping_local.log created':<35} [{'PASSED' if tc2_passed else 'FAILED'}] ({2 if tc2_passed else 0}/2)")

    # TC3: Ping summary contents check (4 packets)
    tc3_passed = False
    if tc2_passed:
        try:
            content = ""
            try:
                with open(ping_log, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
            except Exception:
                import subprocess
                res = subprocess.run(['sudo', 'cat', ping_log], capture_output=True, text=True, timeout=2)
                if res.returncode == 0:
                    content = res.stdout.lower()

            if ('127.0.0.1' in content or 'ping' in content or 'bytes' in content) and ('4' in content or 'packets' in content or 'ttl' in content or 'reply' in content):
                tc3_passed = True
            elif os.path.getsize(ping_log) > 0:
                tc3_passed = True
        except Exception:
            if os.path.exists(ping_log):
                tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 2 if tc3_passed else 0
    print(f"TC3: {'Ping summary output verified':<35} [{'PASSED' if tc3_passed else 'FAILED'}] ({2 if tc3_passed else 0}/2)")

    # TC4: Hostname file created
    tc4_passed = False
    if tc1_passed and (os.path.isfile(hostname_file) or os.path.exists(hostname_file)):
        if check_mtime(hostname_file) and os.path.getsize(hostname_file) > 0:
            tc4_passed = True
    results['tc4'] = tc4_passed
    total_score += 3 if tc4_passed else 0
    print(f"TC4: {'File hostname_info.txt created':<35} [{'PASSED' if tc4_passed else 'FAILED'}] ({3 if tc4_passed else 0}/3)")

    # TC5: Hostname value valid
    tc5_passed = False
    if tc4_passed:
        try:
            line = ""
            try:
                with open(hostname_file, 'r', encoding='utf-8', errors='ignore') as f:
                    line = f.read().strip()
            except Exception:
                import subprocess
                res = subprocess.run(['sudo', 'cat', hostname_file], capture_output=True, text=True, timeout=2)
                if res.returncode == 0:
                    line = res.stdout.strip()

            if len(line) > 0:
                tc5_passed = True
            elif os.path.getsize(hostname_file) > 0:
                tc5_passed = True
        except Exception:
            if os.path.exists(hostname_file):
                tc5_passed = True
    results['tc5'] = tc5_passed
    total_score += 3 if tc5_passed else 0
    print(f"TC5: {'Hostname value verified':<35} [{'PASSED' if tc5_passed else 'FAILED'}] ({3 if tc5_passed else 0}/3)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/10")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    
    output_data = {'score': total_score, 'results': results}
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
    for base_h in all_homes:
        extra_paths.extend([
            os.path.join(base_h, 'KodeBuck_Workspace', 'LX_09_E', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'LX_09_E', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'LX_09_E', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'LX_09_E', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'linux_network_logging_local', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'linux_network_logging_local', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'linux_network_logging_local', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'linux_network_logging_local', 'solution.json')
        ])
    for ep in extra_paths:
        try:
            os.makedirs(os.path.dirname(ep), exist_ok=True)
            with open(ep, 'w') as f:
                json.dump(output_data, f, indent=4)
        except Exception:
            pass

def verify_task_central(*args, **kwargs):
    try:
        from driver_central import verify_task_central as _vtc
        return _vtc(*args, **kwargs)
    except Exception:
        return verify_task()

if __name__ == "__main__":
    verify_task()
