import json
import os
import sys
import stat
import tarfile
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

def find_target_dir(dirname, all_homes):
    # Check /home/ubuntu/dirname first as specified in problem statement
    if os.path.isdir(f'/home/ubuntu/{dirname}'):
        return f'/home/ubuntu/{dirname}'
    for h in all_homes:
        p = os.path.join(h, dirname)
        if os.path.isdir(p):
            return p
    return os.path.join(os.path.expanduser('~'), dirname)

def find_target_file(filename, all_homes, sub_dir=None):
    if sub_dir:
        # Check /home/ubuntu/sub_dir/filename
        p1 = os.path.join(f'/home/ubuntu/{sub_dir}', filename)
        if os.path.isfile(p1) or os.path.exists(p1):
            return p1
        for h in all_homes:
            p = os.path.join(h, sub_dir, filename)
            if os.path.isfile(p) or os.path.exists(p):
                return p
    p2 = os.path.join('/home/ubuntu', filename)
    if os.path.isfile(p2) or os.path.exists(p2):
        return p2
    for h in all_homes:
        p = os.path.join(h, filename)
        if os.path.isfile(p) or os.path.exists(p):
            return p
    return os.path.join(os.path.expanduser('~'), filename)

def get_file_stat(path):
    if not path or not os.path.exists(path):
        return None
    try:
        st = os.stat(path)
        return {
            'mode': stat.S_IMODE(st.st_mode),
            'uid': st.st_uid,
            'gid': st.st_gid
        }
    except Exception:
        try:
            import subprocess
            res = subprocess.run(['sudo', 'stat', '-c', '%a %u %g', path], capture_output=True, text=True, timeout=2)
            if res.returncode == 0:
                parts = res.stdout.strip().split()
                if len(parts) >= 3:
                    return {
                        'mode': int(parts[0], 8),
                        'uid': int(parts[1]),
                        'gid': int(parts[2])
                    }
        except Exception:
            pass
    return None

def get_ownership(path):
    if not path or not os.path.exists(path):
        return None, None
    try:
        import pwd, grp
        st = os.stat(path)
        owner = pwd.getpwuid(st.st_uid).pw_name
        group = grp.getgrgid(st.st_gid).gr_name
        return owner, group
    except Exception:
        try:
            import subprocess
            res = subprocess.run(['sudo', 'stat', '-c', '%U %G', path], capture_output=True, text=True, timeout=2)
            if res.returncode == 0:
                parts = res.stdout.strip().split()
                if len(parts) >= 2:
                    return parts[0], parts[1]
        except Exception:
            pass
    return None, None

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
    print("-" * 60)

    total_score = 0
    results = {}

    all_homes = find_all_user_homes()
    app_dir = find_target_dir('app_data', all_homes)
    conf_file = find_target_file('config_dev.conf', all_homes, sub_dir='app_data')
    key_file = find_target_file('database.key', all_homes, sub_dir='app_data')
    tar_file = find_target_file('app_backup.tar.gz', all_homes)

    # TC1: Environment active
    tc1_passed = any(os.path.isdir(h) for h in all_homes)
    results['tc1'] = tc1_passed
    print(f"TC1: {'Local VM Environment active':<35} [{'PASSED' if tc1_passed else 'FAILED'}] (0/0)")

    # TC2: App directory created with mode 755
    tc2_passed = False
    if tc1_passed and os.path.isdir(app_dir):
        st_data = get_file_stat(app_dir)
        if st_data and st_data['mode'] == 0o755:
            tc2_passed = True
        elif os.path.isdir(app_dir):
            try:
                st = os.stat(app_dir)
                if stat.S_IMODE(st.st_mode) == 0o755:
                    tc2_passed = True
            except Exception:
                pass
    results['tc2'] = tc2_passed
    total_score += 3 if tc2_passed else 0
    print(f"TC2: {'Directory app_data mode 755':<35} [{'PASSED' if tc2_passed else 'FAILED'}] ({3 if tc2_passed else 0}/3)")

    # TC3: Target files created
    tc3_passed = False
    if tc1_passed and os.path.exists(conf_file) and os.path.exists(key_file):
        tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 3 if tc3_passed else 0
    print(f"TC3: {'Files config_dev & database.key':<35} [{'PASSED' if tc3_passed else 'FAILED'}] ({3 if tc3_passed else 0}/3)")

    # TC4: Ownership root:ubuntu
    tc4_passed = False
    if tc3_passed or (os.path.exists(app_dir) and (os.path.exists(conf_file) or os.path.exists(key_file))):
        o_dir, g_dir = get_ownership(app_dir)
        o_conf, g_conf = get_ownership(conf_file)
        o_key, g_key = get_ownership(key_file)
        
        is_root_dir = (o_dir == 'root') or (get_file_stat(app_dir) and get_file_stat(app_dir).get('uid') == 0)
        is_ubuntu_dir = (g_dir == 'ubuntu')
        
        is_root_conf = (o_conf == 'root') or (get_file_stat(conf_file) and get_file_stat(conf_file).get('uid') == 0)
        is_ubuntu_conf = (g_conf == 'ubuntu')
        
        is_root_key = (o_key == 'root') or (get_file_stat(key_file) and get_file_stat(key_file).get('uid') == 0)
        is_ubuntu_key = (g_key == 'ubuntu')

        if (is_root_dir and is_ubuntu_dir) or (is_root_conf and is_ubuntu_conf) or (is_root_key and is_ubuntu_key):
            tc4_passed = True
        elif os.name != 'posix':
            tc4_passed = True
    results['tc4'] = tc4_passed
    total_score += 3 if tc4_passed else 0
    print(f"TC4: {'Ownership set to root:ubuntu':<35} [{'PASSED' if tc4_passed else 'FAILED'}] ({3 if tc4_passed else 0}/3)")

    # TC5: config_dev.conf mode 644
    tc5_passed = False
    if os.path.exists(conf_file):
        st_data = get_file_stat(conf_file)
        if st_data and st_data['mode'] == 0o644:
            tc5_passed = True
        else:
            try:
                st = os.stat(conf_file)
                if stat.S_IMODE(st.st_mode) == 0o644:
                    tc5_passed = True
            except Exception:
                pass
    results['tc5'] = tc5_passed
    total_score += 3 if tc5_passed else 0
    print(f"TC5: {'File config_dev.conf mode 644':<35} [{'PASSED' if tc5_passed else 'FAILED'}] ({3 if tc5_passed else 0}/3)")

    # TC6: database.key mode 400
    tc6_passed = False
    if os.path.exists(key_file):
        st_data = get_file_stat(key_file)
        if st_data and st_data['mode'] == 0o400:
            tc6_passed = True
        else:
            try:
                st = os.stat(key_file)
                if stat.S_IMODE(st.st_mode) == 0o400:
                    tc6_passed = True
            except Exception:
                pass
    results['tc6'] = tc6_passed
    total_score += 4 if tc6_passed else 0
    print(f"TC6: {'File database.key mode 400':<35} [{'PASSED' if tc6_passed else 'FAILED'}] ({4 if tc6_passed else 0}/4)")

    # TC7: Backup archive app_backup.tar.gz created
    tc7_passed = False
    if os.path.isfile(tar_file) and os.path.getsize(tar_file) > 0:
        try:
            with tarfile.open(tar_file, 'r:*') as tar:
                names = tar.getnames()
                if any('app_data' in n or 'config_dev' in n or 'database.key' in n for n in names) or len(names) > 0:
                    tc7_passed = True
        except Exception:
            if os.path.getsize(tar_file) > 0:
                tc7_passed = True
    results['tc7'] = tc7_passed
    total_score += 4 if tc7_passed else 0
    print(f"TC7: {'Backup archive app_backup.tar.gz':<35} [{'PASSED' if tc7_passed else 'FAILED'}] ({4 if tc7_passed else 0}/4)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/20")
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
            os.path.join(base_h, 'KodeBuck_Workspace', 'LX_10_M', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'LX_10_M', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'LX_10_M', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'LX_10_M', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'linux_security_ownership_local', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'linux_security_ownership_local', 'student_workspace', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_Workspace', 'linux_security_ownership_local', 'solution.json'),
            os.path.join(base_h, 'KodeBuck_workspace', 'linux_security_ownership_local', 'solution.json')
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
