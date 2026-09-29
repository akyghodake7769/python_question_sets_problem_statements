import json
import os
import sys
import socket
from datetime import datetime, timezone, timedelta

# Capture Assessment Start Time
START_TIME_STR = os.getenv('KODEBUCK_START_TIME')
START_TIME = None
if START_TIME_STR:
    try:
        START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00'))
    except Exception:
        START_TIME = None

USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', 'LOCAL_USER')

# Fix encoding for consoles printing emojis
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
    print(f"{'KODEBUCK USER NAVIGATION VERIFICATION':^60}")
    print(f"System Hostname: {socket.gethostname()}")
    print("-" * 60)

    total_score = 0
    results = {}

    all_homes = find_all_user_homes()
    workspace_dir = "/var/tmp/backup_workspace"
    initial_file = "/var/tmp/backup_workspace/meta_log.txt"

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

    # --- TC1: Local Environment Verification --- (0 Marks)
    tc1_passed = any(os.path.isdir(h) for h in all_homes)
    results['tc1'] = tc1_passed
    total_score += 0
    print(f"TC1: {'Local Environment active':<35} [{'PASSED' if tc1_passed else 'FAILED'}] (0/0)")

    # --- TC2: Backup Workspace Directory Creation --- (2 Marks)
    tc2_passed = False
    if tc1_passed:
        if os.path.isdir(workspace_dir):
            tc2_passed = True
    results['tc2'] = tc2_passed
    if tc2_passed:
        total_score += 2
    print(f"TC2: {'Backup workspace created':<35} [{'PASSED' if tc2_passed else 'FAILED'}] ({2 if tc2_passed else 0}/2)")

    # Candidate target files
    target_files = [os.path.join(h, "meta_backup.log") for h in all_homes] + ["/home/ubuntu/meta_backup.log"]

    # --- TC3: Initial Log File Creation --- (2 Marks)
    tc3_passed = False
    if tc1_passed:
        if any(os.path.isfile(tf) for tf in target_files) or os.path.isfile(initial_file):
            tc3_passed = True
    results['tc3'] = tc3_passed
    if tc3_passed:
        total_score += 2
    print(f"TC3: {'Initial log file processed':<35} [{'PASSED' if tc3_passed else 'FAILED'}] ({2 if tc3_passed else 0}/2)")

    # --- TC4: File Migration & Renaming --- (3 Marks)
    tc4_passed = False
    if tc1_passed:
        if any(os.path.isfile(tf) for tf in target_files):
            tc4_passed = True
    results['tc4'] = tc4_passed
    if tc4_passed:
        total_score += 3
    print(f"TC4: {'File moved to meta_backup.log':<35} [{'PASSED' if tc4_passed else 'FAILED'}] ({3 if tc4_passed else 0}/3)")

    # --- TC5: Workspace Cleanup Verification --- (3 Marks)
    tc5_passed = False
    if tc1_passed and tc4_passed:
        if not os.path.exists(initial_file):
            tc5_passed = True
    results['tc5'] = tc5_passed
    if tc5_passed:
        total_score += 3
    print(f"TC5: {'Original file cleaned':<35} [{'PASSED' if tc5_passed else 'FAILED'}] ({3 if tc5_passed else 0}/3)")

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
            os.path.join(base_h, 'KodeBuck_Workspace', 'LX_07_E', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'LX_07_E', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'LX_07_E', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'LX_07_E', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'LX_07_E', 'student_workspace', 'solution.py'),
            os.path.join(base_h, 'KodeBuck_workspace', 'LX_07_E', 'student_workspace', 'solution.py'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'linux_user_navigation_local', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'linux_user_navigation_local', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'linux_user_navigation_local', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'linux_user_navigation_local', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'linux_user_navigation_local', 'student_workspace', 'solution.py'),
            os.path.join(base_h, 'KodeBuck_workspace', 'linux_user_navigation_local', 'student_workspace', 'solution.py')
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
