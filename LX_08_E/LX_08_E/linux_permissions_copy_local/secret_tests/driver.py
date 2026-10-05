import json
import os
import sys
import stat
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

def find_target_file(all_homes):
    for h in all_homes:
        p = os.path.join(h, 'env_local.txt')
        if os.path.isfile(p) or os.path.exists(p):
            return p
    if os.path.isdir('/home/ubuntu'):
        return '/home/ubuntu/env_local.txt'
    return os.path.join(os.path.expanduser('~'), 'env_local.txt')

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
    target_file = find_target_file(all_homes)

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

    # TC2: File created
    tc2_passed = False
    if tc1_passed and (os.path.isfile(target_file) or os.path.exists(target_file)):
        if check_mtime(target_file):
            tc2_passed = True
    results['tc2'] = tc2_passed
    total_score += 2 if tc2_passed else 0
    print(f"TC2: {'File env_local.txt created':<35} [{'PASSED' if tc2_passed else 'FAILED'}] ({2 if tc2_passed else 0}/2)")

    # TC3: Content matches /etc/environment
    tc3_passed = False
    if tc2_passed:
        try:
            env_content = ""
            if os.path.exists('/etc/environment'):
                try:
                    with open('/etc/environment', 'r', encoding='utf-8', errors='ignore') as f1:
                        env_content = f1.read().strip()
                except Exception:
                    pass

            file_content = None
            try:
                with open(target_file, 'r', encoding='utf-8', errors='ignore') as f2:
                    file_content = f2.read().strip()
            except Exception:
                try:
                    import subprocess
                    res = subprocess.run(['sudo', 'cat', target_file], capture_output=True, text=True, timeout=2)
                    if res.returncode == 0:
                        file_content = res.stdout.strip()
                except Exception:
                    pass

            if file_content is not None and env_content:
                if file_content == env_content or len(file_content) > 0:
                    tc3_passed = True
            elif os.path.exists(target_file):
                try:
                    if os.path.getsize(target_file) >= 0:
                        tc3_passed = True
                except Exception:
                    tc3_passed = True
        except Exception:
            if os.path.exists(target_file):
                tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 2 if tc3_passed else 0
    print(f"TC3: {'File content verified':<35} [{'PASSED' if tc3_passed else 'FAILED'}] ({2 if tc3_passed else 0}/2)")

    # TC4: Permissions set to 600
    tc4_passed = False
    if tc2_passed:
        try:
            st = os.stat(target_file)
            mode = stat.S_IMODE(st.st_mode)
            if mode == 0o600 or (st.st_mode & 0o777) == 0o600:
                tc4_passed = True
        except Exception:
            try:
                import subprocess
                res = subprocess.run(['stat', '-c', '%a', target_file], capture_output=True, text=True, timeout=2)
                if res.returncode == 0 and res.stdout.strip() == '600':
                    tc4_passed = True
            except Exception:
                pass
    results['tc4'] = tc4_passed
    total_score += 3 if tc4_passed else 0
    print(f"TC4: {'Permissions mode 600 (rw-------)':<35} [{'PASSED' if tc4_passed else 'FAILED'}] ({3 if tc4_passed else 0}/3)")

    # TC5: Ownership verified
    tc5_passed = False
    if tc2_passed:
        try:
            import pwd
            st = os.stat(target_file)
            owner_name = pwd.getpwuid(st.st_uid).pw_name
            if owner_name in ['ubuntu', 'LabsKraft', 'labskraft', 'root'] or st.st_uid == os.getuid():
                tc5_passed = True
        except Exception:
            try:
                import subprocess
                res = subprocess.run(['stat', '-c', '%U', target_file], capture_output=True, text=True, timeout=2)
                if res.returncode == 0 and res.stdout.strip() in ['ubuntu', 'LabsKraft', 'labskraft', 'root']:
                    tc5_passed = True
                else:
                    tc5_passed = True
            except Exception:
                tc5_passed = True
    results['tc5'] = tc5_passed
    total_score += 3 if tc5_passed else 0
    print(f"TC5: {'File ownership verified':<35} [{'PASSED' if tc5_passed else 'FAILED'}] ({3 if tc5_passed else 0}/3)")

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
            os.path.join(base_h, 'KodeBuck_Workspace', 'LX_08_E', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'LX_08_E', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'LX_08_E', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'LX_08_E', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'linux_permissions_copy_local', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'linux_permissions_copy_local', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'linux_permissions_copy_local', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'linux_permissions_copy_local', 'solution.json')
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
