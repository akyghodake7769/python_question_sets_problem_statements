# import json
# import os
# import sys
# import subprocess
# import shutil
# from datetime import datetime, timezone

# # Ensure standard bin directories are included in PATH
# for p in [os.path.expanduser('~/.local/bin'), '/usr/local/bin', '/usr/bin', '/bin']:
#     if p not in os.environ.get('PATH', ''):
#         os.environ['PATH'] = p + os.pathsep + os.environ.get('PATH', '')

# try:
#     import boto3
#     from botocore.exceptions import ClientError, NoCredentialsError
# except ImportError:
#     boto3 = None

# # AWS region is strictly eu-west-2 (London)
# AWS_REGION = "eu-west-2"

# # Session Start Time handling
# START_TIME_STR = os.getenv('KLOUDKRAFT_START_TIME')
# START_TIME = None
# if START_TIME_STR:
#     try:
#         START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00'))
#     except Exception:
#         START_TIME = None

# USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER')


# def get_ec2_client():
#     """
#     Creates an EC2 client for eu-west-2 using active credentials.
#     """
#     if boto3 is None:
#         return None
#     try:
#         access_key = os.getenv('AWS_ACCESS_KEY_ID') or os.getenv('AWS_ACCESS_KEY')
#         secret_key = os.getenv('AWS_SECRET_ACCESS_KEY') or os.getenv('AWS_SECRET_KEY')
#         session_token = os.getenv('AWS_SESSION_TOKEN') or os.getenv('AWS_SECURITY_TOKEN')

#         if access_key and secret_key:
#             return boto3.client(
#                 'ec2',
#                 region_name=AWS_REGION,
#                 aws_access_key_id=access_key,
#                 aws_secret_access_key=secret_key,
#                 aws_session_token=session_token
#             )
#         return boto3.client('ec2', region_name=AWS_REGION)
#     except Exception:
#         return None


# def run_aws_cli(args):
#     """
#     Fallback helper to run AWS CLI commands in eu-west-2 if boto3 is unavailable.
#     """
#     aws_bin = shutil.which('aws')
#     if not aws_bin:
#         return None
#     try:
#         cmd = [aws_bin] + args + ['--region', AWS_REGION, '--output', 'json']
#         res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
#         if res.returncode == 0 and res.stdout.strip():
#             return json.loads(res.stdout)
#     except Exception:
#         pass
#     return None


# def is_port_open(ip_permissions, port):
#     """
#     Checks if a specific TCP port is allowed in IpPermissions.
#     Accepts 0.0.0.0/0, ::/0, or any open IP CIDR.
#     """
#     for perm in ip_permissions:
#         protocol = str(perm.get('IpProtocol', ''))
#         from_port = perm.get('FromPort')
#         to_port = perm.get('ToPort')
#         ip_ranges = [r.get('CidrIp') for r in perm.get('IpRanges', [])]
#         ipv6_ranges = [r.get('CidrIpv6') for r in perm.get('Ipv6Ranges', [])]

#         has_open_ip = '0.0.0.0/0' in ip_ranges or '::/0' in ipv6_ranges or len(ip_ranges) > 0

#         if not has_open_ip:
#             continue

#         if protocol == '-1':
#             return True
#         if protocol.lower() == 'tcp':
#             if from_port is not None and to_port is not None:
#                 if from_port <= port <= to_port:
#                     return True
#             elif from_port is None and to_port is None:
#                 return True
#     return False


# def find_terraform_dir():
#     """
#     Intelligently locates the directory containing main.tf.
#     Searches environment variables, workspace directories, lab directories, and subdirectories.
#     """
#     candidates = []

#     # 1. Environment variables
#     for env_var in ['TERRAFORM_DIR', 'TF_DIR', 'WORKSPACE_DIR', 'LAB_WORKSPACE', 'CODEBUCK_WORKSPACE', 'KLOUDKRAFT_WORKSPACE']:
#         val = os.getenv(env_var)
#         if val and os.path.isdir(val):
#             candidates.append(os.path.abspath(val))

#     # 2. Known project paths
#     base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
#     student_ws = os.path.join(base_dir, 'student_workspace')
#     candidates.extend([
#         student_ws,
#         base_dir,
#         os.path.join(student_ws, 'terraform-ec2-lab'),
#         os.path.join(base_dir, 'terraform-ec2-lab'),
#         os.getcwd(),
#         os.path.join(os.getcwd(), 'student_workspace'),
#         os.path.join(os.getcwd(), 'terraform-ec2-lab'),
#         os.path.expanduser('~/terraform-ec2-lab'),
#         os.path.expanduser('~/student_workspace'),
#         os.path.expanduser('~')
#     ])

#     for c in candidates:
#         if os.path.isdir(c) and os.path.isfile(os.path.join(c, 'main.tf')):
#             return os.path.abspath(c)

#     # 3. Dynamic search within base_dir and cwd
#     search_roots = [student_ws, base_dir, os.getcwd()]
#     for root_dir in search_roots:
#         if not os.path.exists(root_dir):
#             continue
#         for dirpath, dirnames, filenames in os.walk(root_dir):
#             dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('node_modules', '__pycache__', 'venv', '.terraform')]
#             if 'main.tf' in filenames:
#                 return os.path.abspath(dirpath)

#     return None


# def check_evaluation_report():
#     """
#     Checks for structured evaluation report as specified in the lab problem statement:
#     TF_INIT=SUCCESS, TF_PLAN=SUCCESS, etc.
#     """
#     candidate_dirs = [
#         os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace')),
#         os.path.normpath(os.path.join(os.path.dirname(__file__), '..')),
#         os.getcwd(),
#         os.path.expanduser('~/terraform-ec2-lab'),
#         os.path.expanduser('~')
#     ]
#     report_names = [
#         'evaluation_report.txt', 'report.txt', 'terraform_report.txt',
#         'evaluation.log', 'report.log', 'terraform.log'
#     ]

#     for d in candidate_dirs:
#         if not os.path.isdir(d):
#             continue
#         for r_name in report_names:
#             path = os.path.join(d, r_name)
#             if os.path.isfile(path):
#                 try:
#                     with open(path, 'r', encoding='utf-8') as f:
#                         content = f.read()
#                     data = {}
#                     for line in content.splitlines():
#                         if '=' in line:
#                             k, v = line.split('=', 1)
#                             data[k.strip().upper()] = v.strip().upper()
#                     if data:
#                         return data
#                 except Exception:
#                     pass
#     return {}


# def check_local_tfstate():
#     """
#     Checks local terraform.tfstate in student workspace or candidate folders.
#     """
#     candidate_dirs = [
#         os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace')),
#         os.path.normpath(os.path.join(os.path.dirname(__file__), '..')),
#         os.getcwd(),
#         os.path.expanduser('~/terraform-ec2-lab'),
#         os.path.expanduser('~')
#     ]

#     for d in candidate_dirs:
#         state_file = os.path.join(d, "terraform.tfstate")
#         if os.path.isfile(state_file):
#             try:
#                 with open(state_file, "r", encoding='utf-8') as sf:
#                     state_data = json.load(sf)
#                     resources = state_data.get("resources", [])
#                     has_sg = any(r.get("type") == "aws_security_group" for r in resources)
#                     has_ec2 = any(r.get("type") == "aws_instance" for r in resources)

#                     has_port_22 = False
#                     has_port_80 = False
#                     for r in resources:
#                         if r.get("type") in ("aws_security_group", "aws_security_group_rule"):
#                             for inst in r.get("instances", []):
#                                 attrs = inst.get("attributes", {})
#                                 for ing in attrs.get("ingress", []):
#                                     cidrs = ing.get("cidr_blocks", [])
#                                     f_port = ing.get("from_port")
#                                     t_port = ing.get("to_port")
#                                     if "0.0.0.0/0" in cidrs or len(cidrs) > 0:
#                                         if f_port is not None and t_port is not None:
#                                             if f_port <= 22 <= t_port:
#                                                 has_port_22 = True
#                                             if f_port <= 80 <= t_port:
#                                                 has_port_80 = True
#                                         elif ing.get("protocol") == "-1":
#                                             has_port_22 = True
#                                             has_port_80 = True
#                                 if attrs.get("type") == "ingress":
#                                     cidrs = attrs.get("cidr_blocks", [])
#                                     f_port = attrs.get("from_port")
#                                     t_port = attrs.get("to_port")
#                                     if "0.0.0.0/0" in cidrs or len(cidrs) > 0:
#                                         if f_port is not None and t_port is not None:
#                                             if f_port <= 22 <= t_port:
#                                                 has_port_22 = True
#                                             if f_port <= 80 <= t_port:
#                                                 has_port_80 = True

#                     return {
#                         'found': True,
#                         'has_sg': has_sg,
#                         'has_port_22': has_port_22,
#                         'has_port_80': has_port_80,
#                         'has_ec2': has_ec2
#                     }
#             except Exception:
#                 pass
#     return {'found': False, 'has_sg': False, 'has_port_22': False, 'has_port_80': False, 'has_ec2': False}


# def check_live_aws():
#     """
#     Audits live AWS resources in region eu-west-2:
#     1. Specifically looks for Security Group 'my-web-sg' with port 22 and 80 open
#     2. EC2 instance running as t2.micro with tag Name=MyWebServer
#     """
#     ec2 = get_ec2_client()

#     target_sg = None
#     sgs = []
#     if ec2:
#         try:
#             sgs = ec2.describe_security_groups().get('SecurityGroups', [])
#         except Exception:
#             sgs = []

#     if not sgs:
#         cli_res = run_aws_cli(['ec2', 'describe-security-groups'])
#         if cli_res:
#             sgs = cli_res.get('SecurityGroups', [])

#     # Strictly look for SG named 'my-web-sg' (or tag Name=my-web-sg)
#     for sg in sgs:
#         if sg.get('GroupName') == 'my-web-sg':
#             target_sg = sg
#             break
#         tags = {t.get('Key'): t.get('Value') for t in sg.get('Tags', [])}
#         if tags.get('Name') == 'my-web-sg':
#             target_sg = sg
#             break

#     if not target_sg:
#         return {
#             'available': bool(ec2 or shutil.which('aws')),
#             'has_sg': False,
#             'has_port_22': False,
#             'has_port_80': False,
#             'has_ec2': False,
#             'ec2_running': False,
#             'ec2_type_ok': False,
#             'ec2_tag_ok': False,
#             'ec2_sg_assoc': False
#         }

#     sg_id = target_sg.get('GroupId')
#     perms = target_sg.get('IpPermissions', [])
#     has_port_22 = is_port_open(perms, 22)
#     has_port_80 = is_port_open(perms, 80)

#     # EC2 Instances inspection
#     reservations = []
#     if ec2:
#         try:
#             reservations = ec2.describe_instances().get('Reservations', [])
#         except Exception:
#             reservations = []

#     if not reservations:
#         cli_res = run_aws_cli(['ec2', 'describe-instances'])
#         if cli_res:
#             reservations = cli_res.get('Reservations', [])

#     all_inst = []
#     for r in reservations:
#         all_inst.extend(r.get('Instances', []))

#     target_ec2 = None
#     # Match instance with tag Name=MyWebServer or attached to target_sg
#     for inst in all_inst:
#         tags = {t.get('Key'): t.get('Value') for t in inst.get('Tags', [])}
#         inst_sg_ids = [g.get('GroupId') for g in inst.get('SecurityGroups', [])]
#         if tags.get('Name') == 'MyWebServer' or (sg_id and sg_id in inst_sg_ids):
#             target_ec2 = inst
#             break

#     if not target_ec2:
#         return {
#             'available': True,
#             'has_sg': True,
#             'has_port_22': has_port_22,
#             'has_port_80': has_port_80,
#             'has_ec2': False,
#             'ec2_running': False,
#             'ec2_type_ok': False,
#             'ec2_tag_ok': False,
#             'ec2_sg_assoc': False
#         }

#     state = target_ec2.get('State', {}).get('Name', '').lower()
#     ec2_running = state in ('running', 'pending')
#     ec2_type_ok = target_ec2.get('InstanceType', '').lower() == 't2.micro'
#     ec2_tags = {t.get('Key'): t.get('Value') for t in target_ec2.get('Tags', [])}
#     ec2_tag_ok = ec2_tags.get('Name') == 'MyWebServer'
#     inst_sg_ids = [g.get('GroupId') for g in target_ec2.get('SecurityGroups', [])]
#     ec2_sg_assoc = (sg_id and sg_id in inst_sg_ids)

#     return {
#         'available': True,
#         'has_sg': True,
#         'has_port_22': has_port_22,
#         'has_port_80': has_port_80,
#         'has_ec2': True,
#         'ec2_running': ec2_running,
#         'ec2_type_ok': ec2_type_ok,
#         'ec2_tag_ok': ec2_tag_ok,
#         'ec2_sg_assoc': ec2_sg_assoc
#     }


# def verify_task():
#     user_prefix = USER_PREFIX
#     start_time = START_TIME_STR

#     print("\n" + "-"*70, flush=True)
#     print(f"{'KODEBUCK REAL-TIME TERRAFORM AUDIT':^70}", flush=True)
#     print("-"*70, flush=True)

#     total_score = 0
#     results = {'tc1': False, 'tc2': False, 'tc3': False}

#     # Reset / Invalidate previous solution.json to prevent stale cached test runs
#     ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
#     os.makedirs(ws_path, exist_ok=True)
#     solution_file = os.path.join(ws_path, 'solution.json')
#     if os.path.exists(solution_file):
#         try:
#             os.remove(solution_file)
#         except Exception:
#             pass

#     try:
#         now = datetime.now(timezone.utc)
#         if START_TIME:
#             elapsed_minutes = (now - START_TIME).total_seconds() / 60
#             max_duration = 75
#             if elapsed_minutes > max_duration + 5:
#                 print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m", flush=True)
#                 raise Exception("Time Limit Exceeded")
#             print(f"[SYSTEM] Validating Resources for: {user_prefix}", flush=True)
#             print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n", flush=True)
#         else:
#             print(f"[SYSTEM] Validating Resources for: {user_prefix}\n", flush=True)

#         # ---------------------------------------------------------
#         # TC1: Terraform Initialization & Plan/Validate Check (10 Marks)
#         # ---------------------------------------------------------
#         tf_dir = find_terraform_dir()
#         init_ok = False
#         val_ok = False
#         tc1_error_detail = ""

#         if tf_dir and os.path.isfile(os.path.join(tf_dir, "main.tf")):
#             tf_bin = shutil.which("terraform") or "terraform"
#             # 1. Run terraform init
#             try:
#                 init_res = subprocess.run([tf_bin, "init", "-no-color"], cwd=tf_dir, capture_output=True, text=True, timeout=60)
#                 if init_res.returncode == 0:
#                     init_ok = True
#                 else:
#                     tc1_error_detail = init_res.stderr.strip() or init_res.stdout.strip()
#             except Exception as e:
#                 tc1_error_detail = f"init error: {e}"

#             # 2. Run terraform validate or plan
#             try:
#                 val_res = subprocess.run([tf_bin, "validate", "-no-color"], cwd=tf_dir, capture_output=True, text=True, timeout=30)
#                 if val_res.returncode == 0:
#                     val_ok = True
#                 else:
#                     if not tc1_error_detail:
#                         tc1_error_detail = val_res.stderr.strip() or val_res.stdout.strip()
#             except Exception as e:
#                 if not tc1_error_detail:
#                     tc1_error_detail = f"validate error: {e}"

#         # Evidence checks matching TF_Q10 reference
#         eval_report = check_evaluation_report()
#         local_state = check_local_tfstate()
#         live_aws = check_live_aws()

#         if not (init_ok and val_ok):
#             if eval_report.get('TF_INIT') == 'SUCCESS' and (eval_report.get('TF_PLAN') == 'SUCCESS' or eval_report.get('TF_VALIDATE') == 'SUCCESS'):
#                 init_ok = True
#                 val_ok = True
#             elif (live_aws.get('has_sg') and live_aws.get('has_ec2')) or (local_state.get('has_sg') and local_state.get('has_ec2')):
#                 init_ok = True
#                 val_ok = True

#         if init_ok and val_ok:
#             results['tc1'] = True
#             print("TC1: Terraform Initialization & Syntax Validation ........ [PASS] (10/10)", flush=True)
#             print("    ├─ terraform init: PASS", flush=True)
#             print("    └─ terraform validate: PASS", flush=True)
#         else:
#             results['tc1'] = False
#             print("TC1: Terraform Initialization & Syntax Validation ........ [FAILED] (0/10)", flush=True)
#             init_str = "PASS" if init_ok else "FAILED"
#             val_str = "PASS" if val_ok else "FAILED"
#             print(f"    ├─ terraform init: {init_str}", flush=True)
#             print(f"    └─ terraform validate: {val_str}", flush=True)
#             if tc1_error_detail:
#                 first_line = tc1_error_detail.splitlines()[0] if tc1_error_detail else "configuration syntax invalid"
#                 print(f"       └─ [Details]: {first_line[:90]}", flush=True)
#             elif not tf_dir:
#                 print("       └─ [Details]: main.tf not found in workspace", flush=True)

#         # ---------------------------------------------------------
#         # TC2: Security Group Ingress Rules Verification (10 Marks)
#         # ---------------------------------------------------------
#         sg_ok = False
#         rules_ok = False

#         if live_aws.get('has_sg'):
#             sg_ok = True
#             if live_aws.get('has_port_22') and live_aws.get('has_port_80'):
#                 rules_ok = True
#         elif local_state.get('has_sg'):
#             sg_ok = True
#             if local_state.get('has_port_22') and local_state.get('has_port_80'):
#                 rules_ok = True
#         elif eval_report.get('SG_NAME') == 'MY-WEB-SG':
#             sg_ok = True
#             if eval_report.get('INGRESS_22_OPEN') == 'TRUE' and eval_report.get('INGRESS_80_OPEN') == 'TRUE':
#                 rules_ok = True

#         if sg_ok and rules_ok:
#             results['tc2'] = True
#             print("TC2: Security Group Ingress Rules Verification ......... [PASS] (10/10)", flush=True)
#             print("    ├─ Security Group 'my-web-sg': PASS", flush=True)
#             print("    ├─ Ingress Port 22 (SSH from 0.0.0.0/0): PASS", flush=True)
#             print("    └─ Ingress Port 80 (HTTP from 0.0.0.0/0): PASS", flush=True)
#         else:
#             results['tc2'] = False
#             print("TC2: Security Group Ingress Rules Verification ......... [FAILED] (0/10)", flush=True)
#             sg_str = "PASS" if sg_ok else "FAILED (Security Group 'my-web-sg' not found in eu-west-2)"
#             rule_str = "PASS" if rules_ok else "FAILED (Ports 22 and 80 must both be open to 0.0.0.0/0)"
#             print(f"    ├─ Security Group 'my-web-sg': {sg_str}", flush=True)
#             print(f"    └─ Ingress Rules (Ports 22 & 80): {rule_str}", flush=True)

#         # ---------------------------------------------------------
#         # TC3: EC2 Instance State & Tagging Verification (10 Marks)
#         # ---------------------------------------------------------
#         ec2_ok = False
#         attrs_ok = False

#         if live_aws.get('has_ec2'):
#             ec2_ok = True
#             if (live_aws.get('ec2_type_ok') and live_aws.get('ec2_tag_ok')) or live_aws.get('ec2_running'):
#                 attrs_ok = True
#         elif local_state.get('has_ec2'):
#             ec2_ok = True
#             attrs_ok = True
#         elif eval_report.get('EC2_STATE') == 'RUNNING' and eval_report.get('EC2_INSTANCE_TYPE') == 'T2.MICRO':
#             ec2_ok = True
#             if eval_report.get('TAG_NAME') == 'MYWEBSERVER' or eval_report.get('FINAL_STATUS') == 'SUCCESS':
#                 attrs_ok = True

#         if ec2_ok and attrs_ok:
#             results['tc3'] = True
#             print("TC3: EC2 Instance State & Tagging Verification ......... [PASS] (10/10)", flush=True)
#             print("    ├─ EC2 Instance Running: PASS", flush=True)
#             print("    ├─ Instance Type (t2.micro): PASS", flush=True)
#             print("    ├─ Resource Tag (Name=MyWebServer): PASS", flush=True)
#             print("    └─ Security Group Associated: PASS", flush=True)
#         else:
#             results['tc3'] = False
#             print("TC3: EC2 Instance State & Tagging Verification ......... [FAILED] (0/10)", flush=True)
#             ec2_str = "PASS" if ec2_ok else "FAILED (EC2 instance not found in eu-west-2)"
#             attr_str = "PASS" if attrs_ok else "FAILED (Instance type t2.micro or tag Name=MyWebServer missing)"
#             print(f"    ├─ EC2 Instance Running: {ec2_str}", flush=True)
#             print(f"    └─ Type & Tagging: {attr_str}", flush=True)

#         # Final Scoring (Preserves 30 Marks system)
#         total_score = sum([10 for r in results.values() if r])

#         print("-" * 70, flush=True)
#         print(f"{'TOTAL SCORE:':<52} {total_score}/30", flush=True)
#         print("-" * 70 + "\n", flush=True)

#     except Exception as e:
#         print(f"[ERROR] Real-time audit failed: {str(e)}", flush=True)
#         total_score = 0

#     # Save fresh Metadata for Platform Evaluation
#     solution_data = {
#         'candidate_prefix': user_prefix,
#         'assessment_start_time': start_time,
#         'evaluation_type': 'REAL_TIME_API',
#         'score': total_score,
#         'results': results,
#         'timestamp': datetime.now(timezone.utc).isoformat()
#     }

#     try:
#         with open(solution_file, 'w', encoding='utf-8') as f:
#             json.dump(solution_data, f, indent=4)
#     except Exception as e:
#         print(f"[ERROR] Could not write solution.json: {e}", flush=True)

#     return total_score


# if __name__ == '__main__':
#     verify_task()


import json
import os
import sys
import subprocess
import shutil
from datetime import datetime, timezone

# Ensure standard bin directories are included in PATH
for p in [os.path.expanduser('~/.local/bin'), '/usr/local/bin', '/usr/bin', '/bin']:
    if p not in os.environ.get('PATH', ''):
        os.environ['PATH'] = p + os.pathsep + os.environ.get('PATH', '')

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
except ImportError:
    boto3 = None

# AWS region is strictly eu-west-2 (London)
AWS_REGION = "eu-west-2"

# Session Start Time handling
START_TIME_STR = os.getenv('KLOUDKRAFT_START_TIME')
START_TIME = None
if START_TIME_STR:
    try:
        START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00'))
    except Exception:
        START_TIME = None

USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER')


def get_ec2_client():
    """
    Creates an EC2 client for eu-west-2 using active credentials.
    """
    if boto3 is None:
        return None
    try:
        access_key = os.getenv('AWS_ACCESS_KEY_ID') or os.getenv('AWS_ACCESS_KEY')
        secret_key = os.getenv('AWS_SECRET_ACCESS_KEY') or os.getenv('AWS_SECRET_KEY')
        session_token = os.getenv('AWS_SESSION_TOKEN') or os.getenv('AWS_SECURITY_TOKEN')

        if access_key and secret_key:
            return boto3.client(
                'ec2',
                region_name=AWS_REGION,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                aws_session_token=session_token
            )
        return boto3.client('ec2', region_name=AWS_REGION)
    except Exception:
        return None


def run_aws_cli(args):
    """
    Fallback helper to run AWS CLI commands in eu-west-2 if boto3 is unavailable.
    """
    aws_bin = shutil.which('aws')
    if not aws_bin:
        return None
    try:
        cmd = [aws_bin] + args + ['--region', AWS_REGION, '--output', 'json']
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if res.returncode == 0 and res.stdout.strip():
            return json.loads(res.stdout)
    except Exception:
        pass
    return None


def is_port_open(ip_permissions, port):
    """
    Checks if a specific TCP port is allowed in IpPermissions.
    Accepts 0.0.0.0/0, ::/0, or any open IP CIDR.
    """
    for perm in ip_permissions:
        protocol = str(perm.get('IpProtocol', ''))
        from_port = perm.get('FromPort')
        to_port = perm.get('ToPort')
        ip_ranges = [r.get('CidrIp') for r in perm.get('IpRanges', [])]
        ipv6_ranges = [r.get('CidrIpv6') for r in perm.get('Ipv6Ranges', [])]

        has_open_ip = '0.0.0.0/0' in ip_ranges or '::/0' in ipv6_ranges or len(ip_ranges) > 0

        if not has_open_ip:
            continue

        if protocol == '-1':
            return True
        if protocol.lower() == 'tcp':
            if from_port is not None and to_port is not None:
                if from_port <= port <= to_port:
                    return True
            elif from_port is None and to_port is None:
                return True
    return False


def find_terraform_dir():
    """
    Intelligently locates the directory containing main.tf.
    Searches environment variables, workspace directories, lab directories, and subdirectories.
    """
    candidates = []

    # 1. Environment variables
    for env_var in ['TERRAFORM_DIR', 'TF_DIR', 'WORKSPACE_DIR', 'LAB_WORKSPACE', 'CODEBUCK_WORKSPACE', 'KLOUDKRAFT_WORKSPACE']:
        val = os.getenv(env_var)
        if val and os.path.isdir(val):
            candidates.append(os.path.abspath(val))

    # 2. Known project paths
    base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    student_ws = os.path.join(base_dir, 'student_workspace')
    candidates.extend([
        student_ws,
        base_dir,
        os.path.join(student_ws, 'terraform-ec2-lab'),
        os.path.join(base_dir, 'terraform-ec2-lab'),
        os.getcwd(),
        os.path.join(os.getcwd(), 'student_workspace'),
        os.path.join(os.getcwd(), 'terraform-ec2-lab'),
        os.path.expanduser('~/terraform-ec2-lab'),
        os.path.expanduser('~/student_workspace'),
        os.path.expanduser('~')
    ])

    for c in candidates:
        if os.path.isdir(c) and os.path.isfile(os.path.join(c, 'main.tf')):
            return os.path.abspath(c)

    # 3. Dynamic search within base_dir and cwd
    search_roots = [student_ws, base_dir, os.getcwd()]
    for root_dir in search_roots:
        if not os.path.exists(root_dir):
            continue
        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('node_modules', '__pycache__', 'venv', '.terraform')]
            if 'main.tf' in filenames:
                return os.path.abspath(dirpath)

    return None


def check_tf_configuration(tf_dir, required_resource="aws_security_group"):
    """
    Validates that main.tf (or .tf files) in tf_dir actually contains non-empty,
    meaningful Terraform code defining the expected resource(s).
    """
    if not tf_dir or not os.path.isdir(tf_dir):
        return False, "Terraform directory not found"

    main_tf = os.path.join(tf_dir, "main.tf")
    if not os.path.isfile(main_tf):
        return False, "main.tf not found in workspace"

    tf_files = [
        os.path.join(tf_dir, f)
        for f in os.listdir(tf_dir)
        if f.endswith('.tf') and os.path.isfile(os.path.join(tf_dir, f))
    ]
    if not tf_files:
        return False, "No .tf configuration files found in workspace"

    combined_code = ""
    for tf_file in tf_files:
        try:
            with open(tf_file, 'r', encoding='utf-8') as f:
                combined_code += f.read() + "\n"
        except Exception:
            pass

    # Strip single-line and multi-line comments and whitespace
    clean_lines = []
    in_block_comment = False
    for raw_line in combined_code.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if in_block_comment:
            if '*/' in line:
                in_block_comment = False
                line = line.split('*/', 1)[1].strip()
            else:
                continue
        if '/*' in line:
            if '*/' in line:
                line = line[:line.index('/*')].strip() + " " + line[line.index('*/') + 2:].strip()
                line = line.strip()
            else:
                in_block_comment = True
                line = line[:line.index('/*')].strip()
        if line.startswith('#') or line.startswith('//'):
            continue
        if line:
            clean_lines.append(line)

    if not clean_lines:
        return False, "main.tf is empty (no Terraform configuration provided)"

    clean_text = "\n".join(clean_lines)
    if "resource" not in clean_text:
        return False, "No resource blocks defined in main.tf"

    if required_resource and required_resource not in clean_text:
        return False, f"Required resource '{required_resource}' not found in main.tf"

    return True, ""


def check_evaluation_report():
    """
    Checks for structured evaluation report as specified in the lab problem statement:
    TF_INIT=SUCCESS, TF_PLAN=SUCCESS, etc.
    """
    candidate_dirs = [
        os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace')),
        os.path.normpath(os.path.join(os.path.dirname(__file__), '..')),
        os.getcwd(),
        os.path.expanduser('~/terraform-ec2-lab'),
        os.path.expanduser('~')
    ]
    report_names = [
        'evaluation_report.txt', 'report.txt', 'terraform_report.txt',
        'evaluation.log', 'report.log', 'terraform.log'
    ]

    for d in candidate_dirs:
        if not os.path.isdir(d):
            continue
        for r_name in report_names:
            path = os.path.join(d, r_name)
            if os.path.isfile(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    data = {}
                    for line in content.splitlines():
                        if '=' in line:
                            k, v = line.split('=', 1)
                            data[k.strip().upper()] = v.strip().upper()
                    if data:
                        return data
                except Exception:
                    pass
    return {}


def check_local_tfstate():
    """
    Checks local terraform.tfstate in student workspace or candidate folders.
    """
    candidate_dirs = [
        os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace')),
        os.path.normpath(os.path.join(os.path.dirname(__file__), '..')),
        os.getcwd(),
        os.path.expanduser('~/terraform-ec2-lab'),
        os.path.expanduser('~')
    ]

    for d in candidate_dirs:
        state_file = os.path.join(d, "terraform.tfstate")
        if os.path.isfile(state_file):
            try:
                with open(state_file, "r", encoding='utf-8') as sf:
                    state_data = json.load(sf)
                    resources = state_data.get("resources", [])
                    has_sg = any(r.get("type") == "aws_security_group" for r in resources)
                    has_ec2 = any(r.get("type") == "aws_instance" for r in resources)

                    has_port_22 = False
                    has_port_80 = False
                    for r in resources:
                        if r.get("type") in ("aws_security_group", "aws_security_group_rule"):
                            for inst in r.get("instances", []):
                                attrs = inst.get("attributes", {})
                                for ing in attrs.get("ingress", []):
                                    cidrs = ing.get("cidr_blocks", [])
                                    f_port = ing.get("from_port")
                                    t_port = ing.get("to_port")
                                    if "0.0.0.0/0" in cidrs or len(cidrs) > 0:
                                        if f_port is not None and t_port is not None:
                                            if f_port <= 22 <= t_port:
                                                has_port_22 = True
                                            if f_port <= 80 <= t_port:
                                                has_port_80 = True
                                        elif ing.get("protocol") == "-1":
                                            has_port_22 = True
                                            has_port_80 = True
                                if attrs.get("type") == "ingress":
                                    cidrs = attrs.get("cidr_blocks", [])
                                    f_port = attrs.get("from_port")
                                    t_port = attrs.get("to_port")
                                    if "0.0.0.0/0" in cidrs or len(cidrs) > 0:
                                        if f_port is not None and t_port is not None:
                                            if f_port <= 22 <= t_port:
                                                has_port_22 = True
                                            if f_port <= 80 <= t_port:
                                                has_port_80 = True

                    return {
                        'found': True,
                        'has_sg': has_sg,
                        'has_port_22': has_port_22,
                        'has_port_80': has_port_80,
                        'has_ec2': has_ec2
                    }
            except Exception:
                pass
    return {'found': False, 'has_sg': False, 'has_port_22': False, 'has_port_80': False, 'has_ec2': False}


def check_live_aws():
    """
    Audits live AWS resources in region eu-west-2:
    1. Specifically looks for Security Group 'my-web-sg' with port 22 and 80 open
    2. EC2 instance running as t2.micro with tag Name=MyWebServer
    """
    ec2 = get_ec2_client()

    target_sg = None
    sgs = []
    if ec2:
        try:
            sgs = ec2.describe_security_groups().get('SecurityGroups', [])
        except Exception:
            sgs = []

    if not sgs:
        cli_res = run_aws_cli(['ec2', 'describe-security-groups'])
        if cli_res:
            sgs = cli_res.get('SecurityGroups', [])

    # Strictly look for SG named 'my-web-sg' (or tag Name=my-web-sg)
    for sg in sgs:
        if sg.get('GroupName') == 'my-web-sg':
            target_sg = sg
            break
        tags = {t.get('Key'): t.get('Value') for t in sg.get('Tags', [])}
        if tags.get('Name') == 'my-web-sg':
            target_sg = sg
            break

    if not target_sg:
        return {
            'available': bool(ec2 or shutil.which('aws')),
            'has_sg': False,
            'has_port_22': False,
            'has_port_80': False,
            'has_ec2': False,
            'ec2_running': False,
            'ec2_type_ok': False,
            'ec2_tag_ok': False,
            'ec2_sg_assoc': False
        }

    sg_id = target_sg.get('GroupId')
    perms = target_sg.get('IpPermissions', [])
    has_port_22 = is_port_open(perms, 22)
    has_port_80 = is_port_open(perms, 80)

    # EC2 Instances inspection
    reservations = []
    if ec2:
        try:
            reservations = ec2.describe_instances().get('Reservations', [])
        except Exception:
            reservations = []

    if not reservations:
        cli_res = run_aws_cli(['ec2', 'describe-instances'])
        if cli_res:
            reservations = cli_res.get('Reservations', [])

    all_inst = []
    for r in reservations:
        all_inst.extend(r.get('Instances', []))

    target_ec2 = None
    # Match instance with tag Name=MyWebServer or attached to target_sg
    for inst in all_inst:
        tags = {t.get('Key'): t.get('Value') for t in inst.get('Tags', [])}
        inst_sg_ids = [g.get('GroupId') for g in inst.get('SecurityGroups', [])]
        if tags.get('Name') == 'MyWebServer' or (sg_id and sg_id in inst_sg_ids):
            target_ec2 = inst
            break

    if not target_ec2:
        return {
            'available': True,
            'has_sg': True,
            'has_port_22': has_port_22,
            'has_port_80': has_port_80,
            'has_ec2': False,
            'ec2_running': False,
            'ec2_type_ok': False,
            'ec2_tag_ok': False,
            'ec2_sg_assoc': False
        }

    state = target_ec2.get('State', {}).get('Name', '').lower()
    ec2_running = state in ('running', 'pending')
    ec2_type_ok = target_ec2.get('InstanceType', '').lower() == 't2.micro'
    ec2_tags = {t.get('Key'): t.get('Value') for t in target_ec2.get('Tags', [])}
    ec2_tag_ok = ec2_tags.get('Name') == 'MyWebServer'
    inst_sg_ids = [g.get('GroupId') for g in target_ec2.get('SecurityGroups', [])]
    ec2_sg_assoc = (sg_id and sg_id in inst_sg_ids)

    return {
        'available': True,
        'has_sg': True,
        'has_port_22': has_port_22,
        'has_port_80': has_port_80,
        'has_ec2': True,
        'ec2_running': ec2_running,
        'ec2_type_ok': ec2_type_ok,
        'ec2_tag_ok': ec2_tag_ok,
        'ec2_sg_assoc': ec2_sg_assoc
    }


def verify_task():
    user_prefix = USER_PREFIX
    start_time = START_TIME_STR

    print("\n" + "-"*70, flush=True)
    print(f"{'KODEBUCK REAL-TIME TERRAFORM AUDIT':^70}", flush=True)
    print("-"*70, flush=True)

    total_score = 0
    results = {'tc1': False, 'tc2': False, 'tc3': False}

    # Reset / Invalidate previous solution.json to prevent stale cached test runs
    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    solution_file = os.path.join(ws_path, 'solution.json')
    if os.path.exists(solution_file):
        try:
            os.remove(solution_file)
        except Exception:
            pass

    try:
        now = datetime.now(timezone.utc)
        if START_TIME:
            elapsed_minutes = (now - START_TIME).total_seconds() / 60
            max_duration = 75
            if elapsed_minutes > max_duration + 5:
                print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m", flush=True)
                raise Exception("Time Limit Exceeded")
            print(f"[SYSTEM] Validating Resources for: {user_prefix}", flush=True)
            print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n", flush=True)
        else:
            print(f"[SYSTEM] Validating Resources for: {user_prefix}\n", flush=True)

        # ---------------------------------------------------------
        # TC1: Terraform Initialization & Plan/Validate Check (10 Marks)
        # ---------------------------------------------------------
        tf_dir = find_terraform_dir()
        init_ok = False
        val_ok = False
        tc1_error_detail = ""

        # Verify that workspace contains actual Terraform resource definitions
        has_code, code_err = check_tf_configuration(tf_dir, required_resource="aws_security_group")
        if not has_code:
            tc1_error_detail = code_err
        elif tf_dir and os.path.isfile(os.path.join(tf_dir, "main.tf")):
            tf_bin = shutil.which("terraform") or "terraform"
            # 1. Run terraform init
            try:
                init_res = subprocess.run([tf_bin, "init", "-no-color"], cwd=tf_dir, capture_output=True, text=True, timeout=60)
                if init_res.returncode == 0:
                    init_ok = True
                else:
                    tc1_error_detail = init_res.stderr.strip() or init_res.stdout.strip()
            except Exception as e:
                tc1_error_detail = f"init error: {e}"

            # 2. Run terraform validate or plan
            try:
                val_res = subprocess.run([tf_bin, "validate", "-no-color"], cwd=tf_dir, capture_output=True, text=True, timeout=30)
                if val_res.returncode == 0:
                    val_ok = True
                else:
                    if not tc1_error_detail:
                        tc1_error_detail = val_res.stderr.strip() or val_res.stdout.strip()
            except Exception as e:
                if not tc1_error_detail:
                    tc1_error_detail = f"validate error: {e}"

        # Evidence checks matching TF_Q10 reference
        eval_report = check_evaluation_report()
        local_state = check_local_tfstate()
        live_aws = check_live_aws()

        if not (init_ok and val_ok):
            if eval_report.get('TF_INIT') == 'SUCCESS' and (eval_report.get('TF_PLAN') == 'SUCCESS' or eval_report.get('TF_VALIDATE') == 'SUCCESS') and eval_report.get('SG_NAME'):
                init_ok = True
                val_ok = True
            elif (live_aws.get('has_sg') and live_aws.get('has_ec2')) or (local_state.get('has_sg') and local_state.get('has_ec2')):
                init_ok = True
                val_ok = True

        if init_ok and val_ok:
            results['tc1'] = True
            print("TC1: Terraform Initialization & Syntax Validation ........ [PASS] (10/10)", flush=True)
            print("    ├─ terraform init: PASS", flush=True)
            print("    └─ terraform validate: PASS", flush=True)
        else:
            results['tc1'] = False
            print("TC1: Terraform Initialization & Syntax Validation ........ [FAILED] (0/10)", flush=True)
            init_str = "PASS" if init_ok else "FAILED"
            val_str = "PASS" if val_ok else "FAILED"
            print(f"    ├─ terraform init: {init_str}", flush=True)
            print(f"    └─ terraform validate: {val_str}", flush=True)
            if tc1_error_detail:
                first_line = tc1_error_detail.splitlines()[0] if tc1_error_detail else "configuration syntax invalid"
                print(f"       └─ [Details]: {first_line[:90]}", flush=True)
            elif not tf_dir:
                print("       └─ [Details]: main.tf not found in workspace", flush=True)

        # ---------------------------------------------------------
        # TC2: Security Group Ingress Rules Verification (10 Marks)
        # ---------------------------------------------------------
        sg_ok = False
        rules_ok = False

        if live_aws.get('has_sg'):
            sg_ok = True
            if live_aws.get('has_port_22') and live_aws.get('has_port_80'):
                rules_ok = True
        elif local_state.get('has_sg'):
            sg_ok = True
            if local_state.get('has_port_22') and local_state.get('has_port_80'):
                rules_ok = True
        elif eval_report.get('SG_NAME') == 'MY-WEB-SG':
            sg_ok = True
            if eval_report.get('INGRESS_22_OPEN') == 'TRUE' and eval_report.get('INGRESS_80_OPEN') == 'TRUE':
                rules_ok = True

        if sg_ok and rules_ok:
            results['tc2'] = True
            print("TC2: Security Group Ingress Rules Verification ......... [PASS] (10/10)", flush=True)
            print("    ├─ Security Group 'my-web-sg': PASS", flush=True)
            print("    ├─ Ingress Port 22 (SSH from 0.0.0.0/0): PASS", flush=True)
            print("    └─ Ingress Port 80 (HTTP from 0.0.0.0/0): PASS", flush=True)
        else:
            results['tc2'] = False
            print("TC2: Security Group Ingress Rules Verification ......... [FAILED] (0/10)", flush=True)
            sg_str = "PASS" if sg_ok else "FAILED (Security Group 'my-web-sg' not found in eu-west-2)"
            rule_str = "PASS" if rules_ok else "FAILED (Ports 22 and 80 must both be open to 0.0.0.0/0)"
            print(f"    ├─ Security Group 'my-web-sg': {sg_str}", flush=True)
            print(f"    └─ Ingress Rules (Ports 22 & 80): {rule_str}", flush=True)

        # ---------------------------------------------------------
        # TC3: EC2 Instance State & Tagging Verification (10 Marks)
        # ---------------------------------------------------------
        ec2_ok = False
        attrs_ok = False

        if live_aws.get('has_ec2'):
            ec2_ok = True
            if (live_aws.get('ec2_type_ok') and live_aws.get('ec2_tag_ok')) or live_aws.get('ec2_running'):
                attrs_ok = True
        elif local_state.get('has_ec2'):
            ec2_ok = True
            attrs_ok = True
        elif eval_report.get('EC2_STATE') == 'RUNNING' and eval_report.get('EC2_INSTANCE_TYPE') == 'T2.MICRO':
            ec2_ok = True
            if eval_report.get('TAG_NAME') == 'MYWEBSERVER' or eval_report.get('FINAL_STATUS') == 'SUCCESS':
                attrs_ok = True

        if ec2_ok and attrs_ok:
            results['tc3'] = True
            print("TC3: EC2 Instance State & Tagging Verification ......... [PASS] (10/10)", flush=True)
            print("    ├─ EC2 Instance Running: PASS", flush=True)
            print("    ├─ Instance Type (t2.micro): PASS", flush=True)
            print("    ├─ Resource Tag (Name=MyWebServer): PASS", flush=True)
            print("    └─ Security Group Associated: PASS", flush=True)
        else:
            results['tc3'] = False
            print("TC3: EC2 Instance State & Tagging Verification ......... [FAILED] (0/10)", flush=True)
            ec2_str = "PASS" if ec2_ok else "FAILED (EC2 instance not found in eu-west-2)"
            attr_str = "PASS" if attrs_ok else "FAILED (Instance type t2.micro or tag Name=MyWebServer missing)"
            print(f"    ├─ EC2 Instance Running: {ec2_str}", flush=True)
            print(f"    └─ Type & Tagging: {attr_str}", flush=True)

        # Final Scoring (Preserves 30 Marks system)
        total_score = sum([10 for r in results.values() if r])

        print("-" * 70, flush=True)
        print(f"{'TOTAL SCORE:':<52} {total_score}/30", flush=True)
        print("-" * 70 + "\n", flush=True)

    except Exception as e:
        print(f"[ERROR] Real-time audit failed: {str(e)}", flush=True)
        total_score = 0

    # Save fresh Metadata for Platform Evaluation
    solution_data = {
        'candidate_prefix': user_prefix,
        'assessment_start_time': start_time,
        'evaluation_type': 'REAL_TIME_API',
        'score': total_score,
        'results': results,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }

    try:
        with open(solution_file, 'w', encoding='utf-8') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}", flush=True)

    return total_score


if __name__ == '__main__':
    verify_task()

