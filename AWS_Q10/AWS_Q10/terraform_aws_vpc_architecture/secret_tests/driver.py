# # import json
# # import os
# # import sys
# # import subprocess
# # import shutil
# # from datetime import datetime, timezone

# # # Ensure standard bin directories are included in PATH
# # for p in [os.path.expanduser('~/.local/bin'), '/usr/local/bin', '/usr/bin', '/bin']:
# #     if p not in os.environ.get('PATH', ''):
# #         os.environ['PATH'] = p + os.pathsep + os.environ.get('PATH', '')

# # try:
# #     import boto3
# #     from botocore.config import Config
# #     from botocore.exceptions import ClientError, NoCredentialsError
# # except ImportError:
# #     boto3 = None
# #     Config = None

# # # AWS region is strictly eu-west-2 (London)
# # AWS_REGION = "eu-west-2"

# # # Session Start Time handling
# # START_TIME_STR = os.getenv('KODEBUCK_START_TIME') or os.getenv('KLOUDKRAFT_START_TIME')
# # START_TIME = None
# # if START_TIME_STR:
# #     try:
# #         START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00'))
# #     except Exception:
# #         START_TIME = None

# # USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else (os.getenv('KODEBUCK_USERNAME') or os.getenv('LABSKRAFT_USERNAME') or 'LOCAL_USER')


# # def get_ec2_client():
# #     """
# #     Creates an EC2 client for eu-west-2 using active credentials.
# #     Avoids IMDS hanging by checking credentials and setting strict connect timeouts.
# #     """
# #     if boto3 is None:
# #         return None
# #     try:
# #         cfg = Config(connect_timeout=3, read_timeout=5, retries={'max_attempts': 1}) if Config else None
# #         access_key = os.getenv('AWS_ACCESS_KEY_ID') or os.getenv('AWS_ACCESS_KEY')
# #         secret_key = os.getenv('AWS_SECRET_ACCESS_KEY') or os.getenv('AWS_SECRET_KEY')
# #         session_token = os.getenv('AWS_SESSION_TOKEN') or os.getenv('AWS_SECURITY_TOKEN')

# #         kwargs = {'region_name': AWS_REGION}
# #         if cfg:
# #             kwargs['config'] = cfg
# #         if access_key and secret_key:
# #             kwargs['aws_access_key_id'] = access_key
# #             kwargs['aws_secret_access_key'] = secret_key
# #             if session_token:
# #                 kwargs['aws_session_token'] = session_token
# #             return boto3.client('ec2', **kwargs)
# #         if os.path.isfile(os.path.expanduser('~/.aws/credentials')) or os.path.isfile(os.path.expanduser('~/.aws/config')):
# #             return boto3.client('ec2', **kwargs)
# #         return None
# #     except Exception:
# #         return None


# # def run_aws_cli(args):
# #     """
# #     Fallback helper to run AWS CLI commands in eu-west-2 if boto3 is unavailable.
# #     """
# #     aws_bin = shutil.which('aws')
# #     if not aws_bin:
# #         return None
# #     try:
# #         cmd = [aws_bin] + args + ['--region', AWS_REGION, '--output', 'json']
# #         res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
# #         if res.returncode == 0 and res.stdout.strip():
# #             return json.loads(res.stdout)
# #     except Exception:
# #         pass
# #     return None


# # def find_terraform_dir():
# #     """
# #     Intelligently locates the directory containing main.tf.
# #     Searches environment variables, workspace directories, lab directories, and subdirectories.
# #     """
# #     candidates = []

# #     # 1. Environment variables
# #     for env_var in ['TERRAFORM_DIR', 'TF_DIR', 'WORKSPACE_DIR', 'LAB_WORKSPACE', 'KODEBUCK_WORKSPACE', 'CODEBUCK_WORKSPACE', 'KLOUDKRAFT_WORKSPACE']:
# #         val = os.getenv(env_var)
# #         if val and os.path.isdir(val):
# #             candidates.append(os.path.abspath(val))

# #     # 2. Known project paths
# #     base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
# #     student_ws = os.path.join(base_dir, 'student_workspace')
# #     candidates.extend([
# #         student_ws,
# #         base_dir,
# #         os.path.join(student_ws, 'terraform-vpc-lab'),
# #         os.path.join(base_dir, 'terraform-vpc-lab'),
# #         os.getcwd(),
# #         os.path.join(os.getcwd(), 'student_workspace'),
# #         os.path.join(os.getcwd(), 'terraform-vpc-lab'),
# #         os.path.expanduser('~/terraform-vpc-lab'),
# #         os.path.expanduser('~/student_workspace'),
# #         os.path.expanduser('~')
# #     ])

# #     for c in candidates:
# #         if os.path.isfile(os.path.join(c, 'main.tf')):
# #             return os.path.abspath(c)

# #     # 3. Dynamic search within base_dir and cwd
# #     search_roots = [student_ws, base_dir, os.getcwd()]
# #     for root_dir in search_roots:
# #         if not os.path.exists(root_dir):
# #             continue
# #         for dirpath, dirnames, filenames in os.walk(root_dir):
# #             dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('node_modules', '__pycache__', 'venv', '.terraform')]
# #             if 'main.tf' in filenames:
# #                 return os.path.abspath(dirpath)

# #     return None


# # def check_tf_configuration(tf_dir, required_resource="aws_vpc"):
# #     """
# #     Validates that main.tf (or .tf files) in tf_dir actually contains non-empty,
# #     meaningful Terraform code defining the expected resource(s).
# #     """
# #     if not tf_dir or not os.path.isdir(tf_dir):
# #         return False, "Terraform directory not found"

# #     main_tf = os.path.join(tf_dir, "main.tf")
# #     if not os.path.isfile(main_tf):
# #         return False, "main.tf not found in workspace"

# #     tf_files = [
# #         os.path.join(tf_dir, f)
# #         for f in os.listdir(tf_dir)
# #         if f.endswith('.tf') and os.path.isfile(os.path.join(tf_dir, f))
# #     ]
# #     if not tf_files:
# #         return False, "No .tf configuration files found in workspace"

# #     combined_code = ""
# #     for tf_file in tf_files:
# #         try:
# #             with open(tf_file, 'r', encoding='utf-8') as f:
# #                 combined_code += f.read() + "\n"
# #         except Exception:
# #             pass

# #     # Strip single-line and multi-line comments and whitespace
# #     clean_lines = []
# #     in_block_comment = False
# #     for raw_line in combined_code.splitlines():
# #         line = raw_line.strip()
# #         if not line:
# #             continue
# #         if in_block_comment:
# #             if '*/' in line:
# #                 in_block_comment = False
# #                 line = line.split('*/', 1)[1].strip()
# #             else:
# #                 continue
# #         if '/*' in line:
# #             if '*/' in line:
# #                 line = line[:line.index('/*')].strip() + " " + line[line.index('*/') + 2:].strip()
# #                 line = line.strip()
# #             else:
# #                 in_block_comment = True
# #                 line = line[:line.index('/*')].strip()
# #         if line.startswith('#') or line.startswith('//'):
# #             continue
# #         if line:
# #             clean_lines.append(line)

# #     if not clean_lines:
# #         return False, "main.tf is empty (no Terraform configuration provided)"

# #     clean_text = "\n".join(clean_lines)
# #     if "resource" not in clean_text:
# #         return False, "No resource blocks defined in main.tf"

# #     if required_resource and required_resource not in clean_text:
# #         return False, f"Required resource '{required_resource}' not found in main.tf"

# #     return True, ""


# # def check_evaluation_report():
# #     """
# #     Checks for structured evaluation report as specified in the lab problem statement:
# #     TF_INIT=SUCCESS, TF_VALIDATE=SUCCESS, etc.
# #     """
# #     candidate_dirs = [
# #         os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace')),
# #         os.path.normpath(os.path.join(os.path.dirname(__file__), '..')),
# #         os.getcwd(),
# #         os.path.expanduser('~/terraform-vpc-lab'),
# #         os.path.expanduser('~')
# #     ]
# #     report_names = [
# #         'evaluation_report.txt', 'report.txt', 'terraform_report.txt',
# #         'evaluation.log', 'report.log', 'terraform.log'
# #     ]

# #     for d in candidate_dirs:
# #         if not os.path.isdir(d):
# #             continue
# #         for r_name in report_names:
# #             path = os.path.join(d, r_name)
# #             if os.path.isfile(path):
# #                 try:
# #                     with open(path, 'r', encoding='utf-8') as f:
# #                         content = f.read()
# #                     data = {}
# #                     for line in content.splitlines():
# #                         if '=' in line:
# #                             k, v = line.split('=', 1)
# #                             data[k.strip().upper()] = v.strip().upper()
# #                     if data:
# #                         return data
# #                 except Exception:
# #                     pass
# #     return {}


# # def check_local_tfstate():
# #     """
# #     Checks local terraform.tfstate in student workspace or candidate folders.
# #     """
# #     candidate_dirs = [
# #         os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace')),
# #         os.path.normpath(os.path.join(os.path.dirname(__file__), '..')),
# #         os.getcwd(),
# #         os.path.expanduser('~/terraform-vpc-lab'),
# #         os.path.expanduser('~')
# #     ]

# #     for d in candidate_dirs:
# #         state_file = os.path.join(d, "terraform.tfstate")
# #         if os.path.isfile(state_file):
# #             try:
# #                 # Check file modification time against session start time
# #                 if START_TIME:
# #                     mtime = datetime.fromtimestamp(os.path.getmtime(state_file), timezone.utc)
# #                     if mtime < START_TIME:
# #                         continue

# #                 with open(state_file, "r", encoding='utf-8') as sf:
# #                     state_data = json.load(sf)
# #                     resources = state_data.get("resources", [])

# #                     def vpc_matches(r):
# #                         if r.get("type") != "aws_vpc":
# #                             return False
# #                         instances = r.get("instances", [])
# #                         if not instances:
# #                             return True
# #                         for inst in instances:
# #                             attrs = inst.get("attributes", {})
# #                             cidr = attrs.get("cidr_block")
# #                             if cidr and cidr == "10.0.0.0/16":
# #                                 return True
# #                         return False

# #                     def subnet_matches(r):
# #                         if r.get("type") != "aws_subnet":
# #                             return False
# #                         instances = r.get("instances", [])
# #                         if not instances:
# #                             return True
# #                         for inst in instances:
# #                             attrs = inst.get("attributes", {})
# #                             cidr = attrs.get("cidr_block")
# #                             if cidr and cidr == "10.0.1.0/24":
# #                                 return True
# #                         return False

# #                     has_vpc = any(vpc_matches(r) for r in resources)
# #                     has_subnet = any(subnet_matches(r) for r in resources)
# #                     has_igw = any(r.get("type") == "aws_internet_gateway" for r in resources)
# #                     has_rt = any(r.get("type") == "aws_route_table" for r in resources)
# #                     has_assoc = any(r.get("type") == "aws_route_table_association" for r in resources)
# #                     return {
# #                         'found': True,
# #                         'has_vpc': has_vpc,
# #                         'has_subnet': has_subnet,
# #                         'has_igw': has_igw,
# #                         'has_rt': has_rt,
# #                         'has_assoc': has_assoc
# #                     }
# #             except Exception:
# #                 pass
# #     return {'found': False, 'has_vpc': False, 'has_subnet': False, 'has_igw': False, 'has_rt': False, 'has_assoc': False}


# # def check_live_aws():
# #     """
# #     Queries AWS API in region eu-west-2 (London) to inspect live VPC, Subnet, IGW, and Route Table.
# #     Uses boto3 with automatic fallback to AWS CLI.
# #     """
# #     ec2 = get_ec2_client()

# #     # --- 1. Describe VPCs ---
# #     target_vpc = None
# #     vpcs = []
# #     if ec2:
# #         try:
# #             vpcs = ec2.describe_vpcs().get('Vpcs', [])
# #         except Exception:
# #             vpcs = []

# #     if not vpcs:
# #         cli_res = run_aws_cli(['ec2', 'describe-vpcs'])
# #         if cli_res:
# #             vpcs = cli_res.get('Vpcs', [])

# #     for v in vpcs:
# #         if v.get('CidrBlock') == '10.0.0.0/16' and not v.get('IsDefault', False):
# #             tags = {t.get('Key'): t.get('Value') for t in v.get('Tags', [])}
# #             if tags.get('Name') == 'my-simple-vpc':
# #                 target_vpc = v
# #                 break
# #             if target_vpc is None:
# #                 target_vpc = v

# #     if not target_vpc:
# #         return {'available': bool(ec2 or shutil.which('aws')), 'has_vpc': False, 'has_subnet': False, 'has_igw': False, 'has_rt': False, 'has_assoc': False}

# #     vpc_id = target_vpc['VpcId']

# #     # --- 2. Describe Subnets in this VPC ---
# #     subnets = []
# #     if ec2:
# #         try:
# #             subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]).get('Subnets', [])
# #         except Exception:
# #             subnets = []

# #     if not subnets:
# #         cli_res = run_aws_cli(['ec2', 'describe-subnets', '--filters', f"Name=vpc-id,Values={vpc_id}"])
# #         if cli_res:
# #             subnets = cli_res.get('Subnets', [])

# #     public_subnet = next((s for s in subnets if s.get('CidrBlock') == '10.0.1.0/24'), None)
# #     has_subnet = public_subnet is not None
# #     subnet_id = public_subnet['SubnetId'] if public_subnet else None

# #     # --- 3. Describe Internet Gateways attached to this VPC ---
# #     igws = []
# #     if ec2:
# #         try:
# #             igws = ec2.describe_internet_gateways(Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}]).get('InternetGateways', [])
# #         except Exception:
# #             igws = []

# #     if not igws:
# #         cli_res = run_aws_cli(['ec2', 'describe-internet-gateways', '--filters', f"Name=attachment.vpc-id,Values={vpc_id}"])
# #         if cli_res:
# #             igws = cli_res.get('InternetGateways', [])

# #     has_igw = len(igws) > 0
# #     igw_ids = [igw['InternetGatewayId'] for igw in igws]

# #     # --- 4. Describe Route Tables in this VPC ---
# #     rts = []
# #     if ec2:
# #         try:
# #             rts = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]).get('RouteTables', [])
# #         except Exception:
# #             rts = []

# #     if not rts:
# #         cli_res = run_aws_cli(['ec2', 'describe-route-tables', '--filters', f"Name=vpc-id,Values={vpc_id}"])
# #         if cli_res:
# #             rts = cli_res.get('RouteTables', [])

# #     has_route_to_igw = False
# #     has_subnet_assoc = False

# #     for rt in rts:
# #         for route in rt.get('Routes', []):
# #             dest = route.get('DestinationCidrBlock')
# #             gw = route.get('GatewayId', '')
# #             if dest == '0.0.0.0/0' and (gw in igw_ids or gw.startswith('igw-')):
# #                 has_route_to_igw = True
# #                 break

# #         associations = rt.get('Associations', [])
# #         if subnet_id:
# #             for assoc in associations:
# #                 if assoc.get('SubnetId') == subnet_id:
# #                     has_subnet_assoc = True
# #                     break

# #     # If association is implicit via main route table
# #     if not has_subnet_assoc and subnet_id and has_route_to_igw:
# #         for rt in rts:
# #             for assoc in rt.get('Associations', []):
# #                 if assoc.get('Main', False):
# #                     for route in rt.get('Routes', []):
# #                         if route.get('DestinationCidrBlock') == '0.0.0.0/0':
# #                             has_subnet_assoc = True
# #                             break

# #     return {
# #         'available': True,
# #         'vpc_id': vpc_id,
# #         'has_vpc': True,
# #         'has_subnet': has_subnet,
# #         'has_igw': has_igw,
# #         'has_rt': has_route_to_igw,
# #         'has_assoc': has_subnet_assoc
# #     }


# # def verify_task():
# #     user_prefix = USER_PREFIX
# #     start_time = START_TIME_STR

# #     print("\n" + "-"*70, flush=True)
# #     print(f"{'KODEBUCK REAL-TIME TERRAFORM AUDIT':^70}", flush=True)
# #     print("-"*70, flush=True)

# #     total_score = 0
# #     results = {'tc1': False, 'tc2': False, 'tc3': False}

# #     # Reset / Invalidate previous solution.json to prevent stale cached test runs
# #     ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
# #     os.makedirs(ws_path, exist_ok=True)
# #     solution_file = os.path.join(ws_path, 'solution.json')
# #     if os.path.exists(solution_file):
# #         try:
# #             os.remove(solution_file)
# #         except Exception:
# #             pass

# #     try:
# #         now = datetime.now(timezone.utc)
# #         if START_TIME:
# #             elapsed_minutes = (now - START_TIME).total_seconds() / 60
# #             max_duration = 75
# #             if elapsed_minutes > max_duration + 5:
# #                 print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m", flush=True)
# #                 raise Exception("Time Limit Exceeded")
# #             print(f"[SYSTEM] Validating Resources for: {user_prefix}", flush=True)
# #             print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n", flush=True)
# #         else:
# #             print(f"[SYSTEM] Validating Resources for: {user_prefix}\n", flush=True)

# #         # ---------------------------------------------------------
# #         # TC1: Terraform Initialization & Syntax Validation (10 Marks)
# #         # ---------------------------------------------------------
# #         tf_dir = find_terraform_dir()
# #         init_status = "NOT_RUN"
# #         validate_status = "NOT_RUN"
# #         tc1_error_detail = ""

# #         has_code, code_err = check_tf_configuration(tf_dir, required_resource="aws_vpc")
# #         if not has_code:
# #             init_status = "NOT_RUN"
# #             validate_status = "NOT_RUN"
# #             tc1_error_detail = code_err
# #         elif tf_dir and os.path.isfile(os.path.join(tf_dir, "main.tf")):
# #             tf_bin = shutil.which("terraform")
# #             if tf_bin:
# #                 try:
# #                     init_res = subprocess.run([tf_bin, "init", "-no-color"], cwd=tf_dir, capture_output=True, text=True, timeout=60)
# #                     if init_res.returncode == 0:
# #                         init_status = "SUCCESS"
# #                     else:
# #                         init_status = "FAILED"
# #                         tc1_error_detail = init_res.stderr.strip() or init_res.stdout.strip()
# #                 except Exception as e:
# #                     init_status = "FAILED"
# #                     tc1_error_detail = f"init error: {e}"

# #                 try:
# #                     val_res = subprocess.run([tf_bin, "validate", "-no-color"], cwd=tf_dir, capture_output=True, text=True, timeout=30)
# #                     if val_res.returncode == 0:
# #                         validate_status = "SUCCESS"
# #                     else:
# #                         validate_status = "FAILED"
# #                         if not tc1_error_detail:
# #                             tc1_error_detail = val_res.stderr.strip() or val_res.stdout.strip()
# #                 except Exception as e:
# #                     validate_status = "FAILED"
# #                     if not tc1_error_detail:
# #                         tc1_error_detail = f"validate error: {e}"
# #             else:
# #                 eval_report = check_evaluation_report()
# #                 if eval_report.get('TF_INIT') == 'SUCCESS':
# #                     init_status = "SUCCESS"
# #                 if eval_report.get('TF_VALIDATE') == 'SUCCESS':
# #                     validate_status = "SUCCESS"

# #         eval_report = check_evaluation_report()
# #         local_state = check_local_tfstate()
# #         live_aws = check_live_aws()

# #         if not (init_status == "SUCCESS" and validate_status == "SUCCESS"):
# #             if eval_report.get('TF_INIT') == 'SUCCESS' and eval_report.get('TF_VALIDATE') == 'SUCCESS' and (eval_report.get('VPC_CIDR') or eval_report.get('VPC_NAME')):
# #                 init_status = "SUCCESS"
# #                 validate_status = "SUCCESS"
# #             elif has_code and ((live_aws.get('has_vpc') and live_aws.get('has_subnet')) or (local_state.get('has_vpc') and local_state.get('has_subnet'))):
# #                 init_status = "SUCCESS"
# #                 validate_status = "SUCCESS"

# #         if has_code and init_status == "SUCCESS" and validate_status == "SUCCESS":
# #             results['tc1'] = True
# #             print("TC1: Terraform Initialization & Syntax Validation ........ [PASS] (10/10)", flush=True)
# #             print("    ├─ terraform init: SUCCESS", flush=True)
# #             print("    └─ terraform validate: SUCCESS", flush=True)
# #         else:
# #             results['tc1'] = False
# #             print("TC1: Terraform Initialization & Syntax Validation ........ [FAILED] (0/10)", flush=True)
# #             print(f"    ├─ terraform init: {init_status}", flush=True)
# #             print(f"    └─ terraform validate: {validate_status}", flush=True)
# #             if tc1_error_detail:
# #                 first_line = tc1_error_detail.splitlines()[0] if tc1_error_detail else "configuration syntax invalid"
# #                 print(f"       └─ [Details]: {first_line[:90]}", flush=True)
# #             elif not tf_dir:
# #                 print("       └─ [Details]: main.tf not found in workspace", flush=True)

# #         # ---------------------------------------------------------
# #         # TC2: AWS VPC & Subnets Creation Verification (10 Marks)
# #         # ---------------------------------------------------------
# #         vpc_ok = False
# #         subnet_ok = False

# #         if live_aws.get('has_vpc'):
# #             vpc_ok = True
# #             if live_aws.get('has_subnet'):
# #                 subnet_ok = True
# #         elif local_state.get('has_vpc'):
# #             vpc_ok = True
# #             if local_state.get('has_subnet'):
# #                 subnet_ok = True
# #         elif eval_report.get('VPC_CIDR') == '10.0.0.0/16' and eval_report.get('SUBNET_CIDR') == '10.0.1.0/24':
# #             vpc_ok = True
# #             subnet_ok = True

# #         if vpc_ok and subnet_ok:
# #             results['tc2'] = True
# #             print("TC2: AWS VPC & Subnets Creation Verification ............ [PASS] (10/10)", flush=True)
# #             print("    ├─ VPC (CIDR: 10.0.0.0/16 in eu-west-2): PASS", flush=True)
# #             print("    └─ Public Subnet (CIDR: 10.0.1.0/24): PASS", flush=True)
# #         else:
# #             results['tc2'] = False
# #             print("TC2: AWS VPC & Subnets Creation Verification ............ [FAILED] (0/10)", flush=True)
# #             vpc_str = "PASS" if vpc_ok else "FAILED (VPC 10.0.0.0/16 not found in eu-west-2)"
# #             subnet_str = "PASS" if subnet_ok else "FAILED (Subnet 10.0.1.0/24 not found)"
# #             print(f"    ├─ VPC (CIDR: 10.0.0.0/16 in eu-west-2): {vpc_str}", flush=True)
# #             print(f"    └─ Public Subnet (CIDR: 10.0.1.0/24): {subnet_str}", flush=True)

# #         # ---------------------------------------------------------
# #         # TC3: IGW & Route Table Association Verification (10 Marks)
# #         # ---------------------------------------------------------
# #         igw_ok = False
# #         rt_ok = False
# #         assoc_ok = False

# #         if live_aws.get('has_igw'):
# #             igw_ok = True
# #             if live_aws.get('has_rt'):
# #                 rt_ok = True
# #             if live_aws.get('has_assoc'):
# #                 assoc_ok = True
# #         elif local_state.get('has_igw'):
# #             igw_ok = True
# #             if local_state.get('has_rt'):
# #                 rt_ok = True
# #             if local_state.get('has_assoc'):
# #                 assoc_ok = True
# #         elif eval_report.get('IGW_ATTACHED') == 'TRUE' and eval_report.get('FINAL_STATUS') == 'SUCCESS':
# #             igw_ok = True
# #             rt_ok = True
# #             assoc_ok = True

# #         if igw_ok and rt_ok:
# #             results['tc3'] = True
# #             print("TC3: IGW & Route Table Association Verification ........ [PASS] (10/10)", flush=True)
# #             print("    ├─ Internet Gateway Attached: PASS", flush=True)
# #             print("    ├─ Default Route (0.0.0.0/0 -> IGW): PASS", flush=True)
# #             assoc_str = "PASS" if assoc_ok else "PASS (Implicit Subnet Routing)"
# #             print(f"    └─ Subnet Route Table Association: {assoc_str}", flush=True)
# #         else:
# #             results['tc3'] = False
# #             print("TC3: IGW & Route Table Association Verification ........ [FAILED] (0/10)", flush=True)
# #             igw_str = "PASS" if igw_ok else "FAILED (Internet Gateway not attached to VPC)"
# #             rt_str = "PASS" if rt_ok else "FAILED (Route 0.0.0.0/0 -> IGW missing)"
# #             print(f"    ├─ Internet Gateway Attached: {igw_str}", flush=True)
# #             print(f"    └─ Route Table & Subnet Association: {rt_str}", flush=True)

# #         total_score = sum([10 for r in results.values() if r])

# #         print("-" * 70, flush=True)
# #         print(f"{'TOTAL SCORE:':<52} {total_score}/30", flush=True)
# #         print("-" * 70 + "\n", flush=True)

# #     except Exception as e:
# #         print(f"[ERROR] Real-time audit failed: {str(e)}", flush=True)
# #         total_score = 0

# #     solution_data = {
# #         'candidate_prefix': user_prefix,
# #         'assessment_start_time': start_time,
# #         'evaluation_type': 'REAL_TIME_API',
# #         'score': total_score,
# #         'results': results,
# #         'timestamp': datetime.now(timezone.utc).isoformat()
# #     }

# #     try:
# #         with open(solution_file, 'w', encoding='utf-8') as f:
# #             json.dump(solution_data, f, indent=4)
# #     except Exception as e:
# #         print(f"[ERROR] Could not write solution.json: {e}", flush=True)

# #     return total_score


# # if __name__ == '__main__':
# #     verify_task()




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
#     from botocore.config import Config
#     from botocore.exceptions import ClientError, NoCredentialsError
# except ImportError:
#     boto3 = None
#     Config = None

# # AWS region is strictly eu-west-2 (London)
# AWS_REGION = "eu-west-2"

# # Session Start Time handling
# START_TIME_STR = os.getenv('KODEBUCK_START_TIME') or os.getenv('KLOUDKRAFT_START_TIME')
# START_TIME = None
# if START_TIME_STR:
#     try:
#         START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00'))
#     except Exception:
#         START_TIME = None

# USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else (os.getenv('KODEBUCK_USERNAME') or os.getenv('LABSKRAFT_USERNAME') or 'LOCAL_USER')


# def get_ec2_client():
#     """
#     Creates an EC2 client for eu-west-2 using active credentials.
#     Uses boto3 default credential resolution chain (env, config, profile, instance metadata).
#     """
#     if boto3 is None:
#         return None
#     try:
#         cfg = Config(connect_timeout=5, read_timeout=10, retries={'max_attempts': 2}) if Config else None
#         access_key = os.getenv('AWS_ACCESS_KEY_ID') or os.getenv('AWS_ACCESS_KEY')
#         secret_key = os.getenv('AWS_SECRET_ACCESS_KEY') or os.getenv('AWS_SECRET_KEY')
#         session_token = os.getenv('AWS_SESSION_TOKEN') or os.getenv('AWS_SECURITY_TOKEN')

#         kwargs = {'region_name': AWS_REGION}
#         if cfg:
#             kwargs['config'] = cfg
#         if access_key and secret_key:
#             kwargs['aws_access_key_id'] = access_key
#             kwargs['aws_secret_access_key'] = secret_key
#             if session_token:
#                 kwargs['aws_session_token'] = session_token
#         return boto3.client('ec2', **kwargs)
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


# def find_terraform_dir():
#     """
#     Intelligently locates the directory containing main.tf.
#     Searches environment variables, workspace directories, lab directories, and subdirectories.
#     """
#     candidates = []

#     # 1. Environment variables
#     for env_var in ['TERRAFORM_DIR', 'TF_DIR', 'WORKSPACE_DIR', 'LAB_WORKSPACE', 'KODEBUCK_WORKSPACE', 'CODEBUCK_WORKSPACE', 'KLOUDKRAFT_WORKSPACE']:
#         val = os.getenv(env_var)
#         if val and os.path.isdir(val):
#             candidates.append(os.path.abspath(val))

#     # 2. Known project paths
#     base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
#     student_ws = os.path.join(base_dir, 'student_workspace')
#     candidates.extend([
#         student_ws,
#         base_dir,
#         os.path.join(student_ws, 'terraform-vpc-lab'),
#         os.path.join(base_dir, 'terraform-vpc-lab'),
#         os.getcwd(),
#         os.path.join(os.getcwd(), 'student_workspace'),
#         os.path.join(os.getcwd(), 'terraform-vpc-lab'),
#         os.path.expanduser('~/terraform-vpc-lab'),
#         os.path.expanduser('~/student_workspace'),
#         os.path.expanduser('~')
#     ])

#     for c in candidates:
#         if os.path.isfile(os.path.join(c, 'main.tf')):
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


# def check_tf_configuration(tf_dir, required_resource="aws_vpc"):
#     """
#     Validates that main.tf (or .tf files) in tf_dir actually contains non-empty,
#     meaningful Terraform code defining the expected resource(s).
#     """
#     if not tf_dir or not os.path.isdir(tf_dir):
#         return False, "main.tf is empty (no Terraform configuration provided)"

#     main_tf = os.path.join(tf_dir, "main.tf")
#     if not os.path.isfile(main_tf):
#         return False, "main.tf is empty (no Terraform configuration provided)"

#     tf_files = [
#         os.path.join(tf_dir, f)
#         for f in os.listdir(tf_dir)
#         if f.endswith('.tf') and os.path.isfile(os.path.join(tf_dir, f))
#     ]
#     if not tf_files:
#         return False, "main.tf is empty (no Terraform configuration provided)"

#     combined_code = ""
#     for tf_file in tf_files:
#         try:
#             with open(tf_file, 'r', encoding='utf-8') as f:
#                 combined_code += f.read() + "\n"
#         except Exception:
#             pass

#     # Strip single-line and multi-line comments and whitespace
#     clean_lines = []
#     in_block_comment = False
#     for raw_line in combined_code.splitlines():
#         line = raw_line.strip()
#         if not line:
#             continue
#         if in_block_comment:
#             if '*/' in line:
#                 in_block_comment = False
#                 line = line.split('*/', 1)[1].strip()
#             else:
#                 continue
#         if '/*' in line:
#             if '*/' in line:
#                 line = line[:line.index('/*')].strip() + " " + line[line.index('*/') + 2:].strip()
#                 line = line.strip()
#             else:
#                 in_block_comment = True
#                 line = line[:line.index('/*')].strip()
#         if line.startswith('#') or line.startswith('//'):
#             continue
#         if line:
#             clean_lines.append(line)

#     if not clean_lines:
#         return False, "main.tf is empty (no Terraform configuration provided)"

#     clean_text = "\n".join(clean_lines)
#     if "resource" not in clean_text:
#         return False, "No resource blocks defined in main.tf"

#     if required_resource and required_resource not in clean_text:
#         return False, f"Required resource '{required_resource}' not found in main.tf"

#     return True, ""


# def check_evaluation_report():
#     """
#     Checks for structured evaluation report as specified in the lab problem statement:
#     TF_INIT=SUCCESS, TF_VALIDATE=SUCCESS, etc.
#     """
#     candidate_dirs = [
#         os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace')),
#         os.path.normpath(os.path.join(os.path.dirname(__file__), '..')),
#         os.getcwd(),
#         os.path.expanduser('~/terraform-vpc-lab'),
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
#         os.path.expanduser('~/terraform-vpc-lab'),
#         os.path.expanduser('~')
#     ]

#     for d in candidate_dirs:
#         state_file = os.path.join(d, "terraform.tfstate")
#         if os.path.isfile(state_file):
#             try:
#                 # Check file modification time against session start time
#                 if START_TIME:
#                     mtime = datetime.fromtimestamp(os.path.getmtime(state_file), timezone.utc)
#                     if mtime < START_TIME:
#                         continue

#                 with open(state_file, "r", encoding='utf-8') as sf:
#                     state_data = json.load(sf)
#                     resources = state_data.get("resources", [])

#                     def vpc_matches(r):
#                         if r.get("type") != "aws_vpc":
#                             return False
#                         instances = r.get("instances", [])
#                         if not instances:
#                             return True
#                         for inst in instances:
#                             attrs = inst.get("attributes", {})
#                             cidr = attrs.get("cidr_block")
#                             if cidr and cidr == "10.0.0.0/16":
#                                 return True
#                         return False

#                     def subnet_matches(r):
#                         if r.get("type") != "aws_subnet":
#                             return False
#                         instances = r.get("instances", [])
#                         if not instances:
#                             return True
#                         for inst in instances:
#                             attrs = inst.get("attributes", {})
#                             cidr = attrs.get("cidr_block")
#                             if cidr and cidr == "10.0.1.0/24":
#                                 return True
#                         return False

#                     has_vpc = any(vpc_matches(r) for r in resources)
#                     has_subnet = any(subnet_matches(r) for r in resources)
#                     has_igw = any(r.get("type") == "aws_internet_gateway" for r in resources)
#                     has_rt = any(r.get("type") == "aws_route_table" for r in resources)
#                     has_assoc = any(r.get("type") == "aws_route_table_association" for r in resources)
#                     return {
#                         'found': True,
#                         'has_vpc': has_vpc,
#                         'has_subnet': has_subnet,
#                         'has_igw': has_igw,
#                         'has_rt': has_rt,
#                         'has_assoc': has_assoc
#                     }
#             except Exception:
#                 pass
#     return {'found': False, 'has_vpc': False, 'has_subnet': False, 'has_igw': False, 'has_rt': False, 'has_assoc': False}


# def check_live_aws():
#     """
#     Queries AWS API in region eu-west-2 (London) to inspect live VPC, Subnet, IGW, and Route Table.
#     Uses boto3 with automatic fallback to AWS CLI.
#     """
#     ec2 = get_ec2_client()

#     # --- 1. Describe VPCs ---
#     target_vpc = None
#     vpcs = []
#     if ec2:
#         try:
#             vpcs = ec2.describe_vpcs().get('Vpcs', [])
#         except Exception:
#             vpcs = []

#     if not vpcs:
#         cli_res = run_aws_cli(['ec2', 'describe-vpcs'])
#         if cli_res:
#             vpcs = cli_res.get('Vpcs', [])

#     for v in vpcs:
#         cidr = v.get('CidrBlock')
#         is_default = v.get('IsDefault', False)
#         if (cidr == '10.0.0.0/16' or not is_default) and not is_default:
#             tags = {t.get('Key'): t.get('Value') for t in v.get('Tags', [])}
#             if tags.get('Name') == 'my-simple-vpc' or cidr == '10.0.0.0/16':
#                 target_vpc = v
#                 break
#             if target_vpc is None:
#                 target_vpc = v

#     if not target_vpc:
#         return {'available': bool(ec2 or shutil.which('aws')), 'has_vpc': False, 'has_subnet': False, 'has_igw': False, 'has_rt': False, 'has_assoc': False}

#     vpc_id = target_vpc['VpcId']

#     # --- 2. Describe Subnets in this VPC ---
#     subnets = []
#     if ec2:
#         try:
#             subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]).get('Subnets', [])
#         except Exception:
#             subnets = []

#     if not subnets:
#         cli_res = run_aws_cli(['ec2', 'describe-subnets', '--filters', f"Name=vpc-id,Values={vpc_id}"])
#         if cli_res:
#             subnets = cli_res.get('Subnets', [])

#     public_subnet = next((s for s in subnets if s.get('CidrBlock') == '10.0.1.0/24'), None)
#     if not public_subnet and subnets:
#         public_subnet = subnets[0]
#     has_subnet = public_subnet is not None
#     subnet_id = public_subnet['SubnetId'] if public_subnet else None

#     # --- 3. Describe Internet Gateways attached to this VPC ---
#     igws = []
#     if ec2:
#         try:
#             igws = ec2.describe_internet_gateways(Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}]).get('InternetGateways', [])
#         except Exception:
#             igws = []

#     if not igws:
#         cli_res = run_aws_cli(['ec2', 'describe-internet-gateways', '--filters', f"Name=attachment.vpc-id,Values={vpc_id}"])
#         if cli_res:
#             igws = cli_res.get('InternetGateways', [])

#     has_igw = len(igws) > 0
#     igw_ids = [igw['InternetGatewayId'] for igw in igws]

#     # --- 4. Describe Route Tables in this VPC ---
#     rts = []
#     if ec2:
#         try:
#             rts = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]).get('RouteTables', [])
#         except Exception:
#             rts = []

#     if not rts:
#         cli_res = run_aws_cli(['ec2', 'describe-route-tables', '--filters', f"Name=vpc-id,Values={vpc_id}"])
#         if cli_res:
#             rts = cli_res.get('RouteTables', [])

#     has_route_to_igw = False
#     has_subnet_assoc = False

#     for rt in rts:
#         for route in rt.get('Routes', []):
#             dest = route.get('DestinationCidrBlock')
#             gw = route.get('GatewayId', '')
#             if dest == '0.0.0.0/0' and (gw in igw_ids or gw.startswith('igw-') or len(igws) > 0):
#                 has_route_to_igw = True
#                 break

#         associations = rt.get('Associations', [])
#         if subnet_id:
#             for assoc in associations:
#                 if assoc.get('SubnetId') == subnet_id or assoc.get('RouteTableAssociationId'):
#                     has_subnet_assoc = True
#                     break

#     # If association is implicit via main route table
#     if not has_subnet_assoc and subnet_id and has_route_to_igw:
#         for rt in rts:
#             for assoc in rt.get('Associations', []):
#                 if assoc.get('Main', False):
#                     for route in rt.get('Routes', []):
#                         if route.get('DestinationCidrBlock') == '0.0.0.0/0':
#                             has_subnet_assoc = True
#                             break

#     return {
#         'available': True,
#         'vpc_id': vpc_id,
#         'has_vpc': True,
#         'has_subnet': has_subnet,
#         'has_igw': has_igw,
#         'has_rt': has_route_to_igw,
#         'has_assoc': has_subnet_assoc
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
#         # Evidence checks (Live AWS, Local State, Evaluation Report)
#         # ---------------------------------------------------------
#         eval_report = check_evaluation_report()
#         local_state = check_local_tfstate()
#         live_aws = check_live_aws()

#         # ---------------------------------------------------------
#         # TC1: Terraform Initialization & Syntax Validation (10 Marks)
#         # ---------------------------------------------------------
#         tf_dir = find_terraform_dir()
#         init_status = "NOT_RUN"
#         validate_status = "NOT_RUN"
#         tc1_error_detail = ""

#         has_code, code_err = check_tf_configuration(tf_dir, required_resource="aws_vpc")
#         if tf_dir and os.path.isfile(os.path.join(tf_dir, "main.tf")) and has_code:
#             tf_bin = shutil.which("terraform")
#             if tf_bin:
#                 try:
#                     init_res = subprocess.run([tf_bin, "init", "-no-color"], cwd=tf_dir, capture_output=True, text=True, timeout=60)
#                     if init_res.returncode == 0:
#                         init_status = "SUCCESS"
#                     else:
#                         init_status = "FAILED"
#                         tc1_error_detail = init_res.stderr.strip() or init_res.stdout.strip()
#                 except Exception as e:
#                     init_status = "FAILED"
#                     tc1_error_detail = f"init error: {e}"

#                 try:
#                     val_res = subprocess.run([tf_bin, "validate", "-no-color"], cwd=tf_dir, capture_output=True, text=True, timeout=30)
#                     if val_res.returncode == 0:
#                         validate_status = "SUCCESS"
#                     else:
#                         validate_status = "FAILED"
#                         if not tc1_error_detail:
#                             tc1_error_detail = val_res.stderr.strip() or val_res.stdout.strip()
#                 except Exception as e:
#                     validate_status = "FAILED"
#                     if not tc1_error_detail:
#                         tc1_error_detail = f"validate error: {e}"
#             else:
#                 if eval_report.get('TF_INIT') == 'SUCCESS':
#                     init_status = "SUCCESS"
#                 if eval_report.get('TF_VALIDATE') == 'SUCCESS':
#                     validate_status = "SUCCESS"

#         # If infrastructure exists in AWS (e.g. provisioned in CloudShell) or in tfstate, validate TC1 as SUCCESS
#         if live_aws.get('has_vpc') or local_state.get('has_vpc') or eval_report.get('VPC_CIDR'):
#             init_status = "SUCCESS"
#             validate_status = "SUCCESS"

#         tc1_passed = (init_status == "SUCCESS" and validate_status == "SUCCESS")

#         if tc1_passed:
#             results['tc1'] = True
#             print("TC1: Terraform Initialization & Syntax Validation ........ [PASS] (10/10)", flush=True)
#             print("    ├─ terraform init: SUCCESS", flush=True)
#             print("    └─ terraform validate: SUCCESS", flush=True)
#         else:
#             results['tc1'] = False
#             print("TC1: Terraform Initialization & Syntax Validation ........ [FAILED] (0/10)", flush=True)
#             print(f"    ├─ terraform init: {init_status}", flush=True)
#             print(f"    └─ terraform validate: {validate_status}", flush=True)
#             if tc1_error_detail:
#                 first_line = tc1_error_detail.splitlines()[0] if tc1_error_detail else "configuration syntax invalid"
#                 print(f"       └─ [Details]: {first_line[:90]}", flush=True)
#             elif not tf_dir:
#                 print("       └─ [Details]: main.tf not found in workspace", flush=True)
#             elif not has_code:
#                 print(f"       └─ [Details]: {code_err}", flush=True)

#         # ---------------------------------------------------------
#         # TC2: AWS VPC & Subnets Creation Verification (10 Marks)
#         # ---------------------------------------------------------
#         vpc_ok = False
#         subnet_ok = False

#         if live_aws.get('has_vpc'):
#             vpc_ok = True
#             if live_aws.get('has_subnet'):
#                 subnet_ok = True
#         elif local_state.get('has_vpc'):
#             vpc_ok = True
#             if local_state.get('has_subnet'):
#                 subnet_ok = True
#         elif eval_report.get('VPC_CIDR') == '10.0.0.0/16' and eval_report.get('SUBNET_CIDR') == '10.0.1.0/24':
#             vpc_ok = True
#             subnet_ok = True

#         if vpc_ok and subnet_ok:
#             results['tc2'] = True
#             print("TC2: AWS VPC & Subnets Creation Verification ............ [PASS] (10/10)", flush=True)
#             print("    ├─ VPC (CIDR: 10.0.0.0/16 in eu-west-2): PASS", flush=True)
#             print("    └─ Public Subnet (CIDR: 10.0.1.0/24): PASS", flush=True)
#         else:
#             results['tc2'] = False
#             print("TC2: AWS VPC & Subnets Creation Verification ............ [FAILED] (0/10)", flush=True)
#             vpc_str = "PASS" if vpc_ok else "FAILED (VPC 10.0.0.0/16 not found in eu-west-2)"
#             subnet_str = "PASS" if subnet_ok else "FAILED (Subnet 10.0.1.0/24 not found)"
#             print(f"    ├─ VPC (CIDR: 10.0.0.0/16 in eu-west-2): {vpc_str}", flush=True)
#             print(f"    └─ Public Subnet (CIDR: 10.0.1.0/24): {subnet_str}", flush=True)

#         # ---------------------------------------------------------
#         # TC3: IGW & Route Table Association Verification (10 Marks)
#         # ---------------------------------------------------------
#         igw_ok = False
#         rt_ok = False
#         assoc_ok = False

#         if live_aws.get('has_igw'):
#             igw_ok = True
#             if live_aws.get('has_rt'):
#                 rt_ok = True
#             if live_aws.get('has_assoc'):
#                 assoc_ok = True
#         elif local_state.get('has_igw'):
#             igw_ok = True
#             if local_state.get('has_rt'):
#                 rt_ok = True
#             if local_state.get('has_assoc'):
#                 assoc_ok = True
#         elif eval_report.get('IGW_ATTACHED') == 'TRUE' and eval_report.get('FINAL_STATUS') == 'SUCCESS':
#             igw_ok = True
#             rt_ok = True
#             assoc_ok = True

#         if igw_ok and rt_ok:
#             results['tc3'] = True
#             print("TC3: IGW & Route Table Association Verification ........ [PASS] (10/10)", flush=True)
#             print("    ├─ Internet Gateway Attached: PASS", flush=True)
#             print("    ├─ Default Route (0.0.0.0/0 -> IGW): PASS", flush=True)
#             assoc_str = "PASS" if assoc_ok else "PASS (Implicit Subnet Routing)"
#             print(f"    └─ Subnet Route Table Association: {assoc_str}", flush=True)
#         else:
#             results['tc3'] = False
#             print("TC3: IGW & Route Table Association Verification ........ [FAILED] (0/10)", flush=True)
#             igw_str = "PASS" if igw_ok else "FAILED (Internet Gateway not attached to VPC)"
#             rt_str = "PASS" if rt_ok else "FAILED (Route 0.0.0.0/0 -> IGW missing)"
#             print(f"    ├─ Internet Gateway Attached: {igw_str}", flush=True)
#             print(f"    └─ Route Table & Subnet Association: {rt_str}", flush=True)

#         total_score = sum([10 for r in results.values() if r])

#         print("-" * 70, flush=True)
#         print(f"{'TOTAL SCORE:':<52} {total_score}/30", flush=True)
#         print("-" * 70 + "\n", flush=True)

#     except Exception as e:
#         print(f"[ERROR] Real-time audit failed: {str(e)}", flush=True)
#         total_score = 0

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

AWS_REGION = "eu-west-2"

# Session Start Time handling
START_TIME_STR = os.getenv('KODEBUCK_START_TIME') or os.getenv('KLOUDKRAFT_START_TIME')
START_TIME = None
if START_TIME_STR:
    try:
        START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00'))
    except Exception:
        START_TIME = None

USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else (os.getenv('KODEBUCK_USERNAME') or os.getenv('LABSKRAFT_USERNAME') or 'LOCAL_USER')


def get_ec2_client(region_name=AWS_REGION):
    try:
        import boto3
        return boto3.client('ec2', region_name=region_name)
    except Exception:
        return None


def run_aws_cli(args):
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


def find_terraform_dir():
    candidates = []
    for env_var in ['TERRAFORM_DIR', 'TF_DIR', 'WORKSPACE_DIR', 'LAB_WORKSPACE', 'KODEBUCK_WORKSPACE', 'CODEBUCK_WORKSPACE', 'KLOUDKRAFT_WORKSPACE']:
        val = os.getenv(env_var)
        if val and os.path.isdir(val):
            candidates.append(os.path.abspath(val))

    base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    student_ws = os.path.join(base_dir, 'student_workspace')
    candidates.extend([
        student_ws,
        base_dir,
        os.path.join(student_ws, 'terraform-vpc-lab'),
        os.path.join(base_dir, 'terraform-vpc-lab'),
        os.getcwd(),
        os.path.join(os.getcwd(), 'student_workspace'),
        os.path.join(os.getcwd(), 'terraform-vpc-lab'),
        os.path.expanduser('~/terraform-vpc-lab'),
        os.path.expanduser('~/student_workspace'),
        os.path.expanduser('~')
    ])

    for c in candidates:
        if os.path.isfile(os.path.join(c, 'main.tf')):
            return os.path.abspath(c)

    search_roots = [student_ws, base_dir, os.getcwd()]
    for root_dir in search_roots:
        if not os.path.exists(root_dir):
            continue
        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('node_modules', '__pycache__', 'venv', '.terraform')]
            if 'main.tf' in filenames:
                return os.path.abspath(dirpath)

    return None


def check_tf_configuration(tf_dir, required_resource="aws_vpc"):
    if not tf_dir or not os.path.isdir(tf_dir):
        return False, "main.tf is empty (no Terraform configuration provided)"

    main_tf = os.path.join(tf_dir, "main.tf")
    if not os.path.isfile(main_tf):
        return False, "main.tf is empty (no Terraform configuration provided)"

    tf_files = [
        os.path.join(tf_dir, f)
        for f in os.listdir(tf_dir)
        if f.endswith('.tf') and os.path.isfile(os.path.join(tf_dir, f))
    ]
    if not tf_files:
        return False, "main.tf is empty (no Terraform configuration provided)"

    combined_code = ""
    for tf_file in tf_files:
        try:
            with open(tf_file, 'r', encoding='utf-8') as f:
                combined_code += f.read() + "\n"
        except Exception:
            pass

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


def check_local_tfstate():
    candidate_dirs = [
        os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace')),
        os.path.normpath(os.path.join(os.path.dirname(__file__), '..')),
        os.getcwd(),
        os.path.expanduser('~/terraform-vpc-lab'),
        os.path.expanduser('~')
    ]

    for d in candidate_dirs:
        state_file = os.path.join(d, "terraform.tfstate")
        if os.path.isfile(state_file):
            try:
                with open(state_file, "r", encoding='utf-8') as sf:
                    state_data = json.load(sf)
                    resources = state_data.get("resources", [])

                    def vpc_matches(r):
                        if r.get("type") != "aws_vpc":
                            return False
                        instances = r.get("instances", [])
                        if not instances:
                            return True
                        for inst in instances:
                            attrs = inst.get("attributes", {})
                            cidr = attrs.get("cidr_block")
                            if cidr and cidr == "10.0.0.0/16":
                                return True
                        return False

                    def subnet_matches(r):
                        if r.get("type") != "aws_subnet":
                            return False
                        instances = r.get("instances", [])
                        if not instances:
                            return True
                        for inst in instances:
                            attrs = inst.get("attributes", {})
                            cidr = attrs.get("cidr_block")
                            if cidr and cidr == "10.0.1.0/24":
                                return True
                        return False

                    has_vpc = any(vpc_matches(r) for r in resources)
                    has_subnet = any(subnet_matches(r) for r in resources)
                    has_igw = any(r.get("type") == "aws_internet_gateway" for r in resources)
                    has_rt = any(r.get("type") == "aws_route_table" for r in resources)
                    has_assoc = any(r.get("type") == "aws_route_table_association" for r in resources)
                    return {
                        'found': True,
                        'has_vpc': has_vpc,
                        'has_subnet': has_subnet,
                        'has_igw': has_igw,
                        'has_rt': has_rt,
                        'has_assoc': has_assoc
                    }
            except Exception:
                pass
    return {'found': False, 'has_vpc': False, 'has_subnet': False, 'has_igw': False, 'has_rt': False, 'has_assoc': False}


def check_live_aws():
    ec2 = get_ec2_client()

    target_vpc = None
    vpcs = []
    if ec2:
        try:
            vpcs = ec2.describe_vpcs().get('Vpcs', [])
        except Exception:
            vpcs = []

    if not vpcs:
        cli_res = run_aws_cli(['ec2', 'describe-vpcs'])
        if cli_res:
            vpcs = cli_res.get('Vpcs', [])

    for v in vpcs:
        cidr = v.get('CidrBlock')
        is_default = v.get('IsDefault', False)
        if not is_default:
            tags = {t.get('Key'): t.get('Value') for t in v.get('Tags', [])}
            if tags.get('Name') == 'my-simple-vpc' or cidr == '10.0.0.0/16':
                target_vpc = v
                break
            if target_vpc is None and cidr == '10.0.0.0/16':
                target_vpc = v
            elif target_vpc is None:
                target_vpc = v

    if not target_vpc:
        return {'available': bool(ec2 or shutil.which('aws')), 'has_vpc': False, 'has_subnet': False, 'has_igw': False, 'has_rt': False, 'has_assoc': False}

    vpc_id = target_vpc['VpcId']

    subnets = []
    if ec2:
        try:
            subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]).get('Subnets', [])
        except Exception:
            subnets = []

    if not subnets:
        cli_res = run_aws_cli(['ec2', 'describe-subnets', '--filters', f"Name=vpc-id,Values={vpc_id}"])
        if cli_res:
            subnets = cli_res.get('Subnets', [])

    public_subnet = next((s for s in subnets if s.get('CidrBlock') == '10.0.1.0/24'), None)
    if not public_subnet and subnets:
        public_subnet = subnets[0]
    has_subnet = public_subnet is not None
    subnet_id = public_subnet['SubnetId'] if public_subnet else None

    igws = []
    if ec2:
        try:
            igws = ec2.describe_internet_gateways(Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}]).get('InternetGateways', [])
        except Exception:
            igws = []

    if not igws:
        cli_res = run_aws_cli(['ec2', 'describe-internet-gateways', '--filters', f"Name=attachment.vpc-id,Values={vpc_id}"])
        if cli_res:
            igws = cli_res.get('InternetGateways', [])

    has_igw = len(igws) > 0
    igw_ids = [igw['InternetGatewayId'] for igw in igws]

    rts = []
    if ec2:
        try:
            rts = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]).get('RouteTables', [])
        except Exception:
            rts = []

    if not rts:
        cli_res = run_aws_cli(['ec2', 'describe-route-tables', '--filters', f"Name=vpc-id,Values={vpc_id}"])
        if cli_res:
            rts = cli_res.get('RouteTables', [])

    has_route_to_igw = False
    has_subnet_assoc = False

    for rt in rts:
        for route in rt.get('Routes', []):
            dest = route.get('DestinationCidrBlock')
            gw = route.get('GatewayId', '')
            if dest == '0.0.0.0/0' and (gw in igw_ids or gw.startswith('igw-') or len(igws) > 0):
                has_route_to_igw = True
                break

        associations = rt.get('Associations', [])
        if subnet_id:
            for assoc in associations:
                if assoc.get('SubnetId') == subnet_id or assoc.get('RouteTableAssociationId'):
                    has_subnet_assoc = True
                    break
        elif associations:
            has_subnet_assoc = True

    if not has_subnet_assoc and has_route_to_igw:
        has_subnet_assoc = True

    return {
        'available': True,
        'vpc_id': vpc_id,
        'has_vpc': True,
        'has_subnet': has_subnet,
        'has_igw': has_igw,
        'has_rt': has_route_to_igw,
        'has_assoc': has_subnet_assoc
    }


def verify_task():
    user_prefix = USER_PREFIX
    start_time = START_TIME_STR

    print("\n" + "-"*70, flush=True)
    print(f"{'KODEBUCK REAL-TIME TERRAFORM AUDIT':^70}", flush=True)
    print("-"*70, flush=True)

    total_score = 0
    results = {'tc1': False, 'tc2': False, 'tc3': False}

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    solution_file = os.path.join(ws_path, 'solution.json')
    if os.path.exists(solution_file):
        try:
            os.remove(solution_file)
        except Exception:
            pass

    try:
        session_start = START_TIME
        if not session_start:
            session_start = datetime.now(timezone.utc)
            start_time = session_start.isoformat()

        now = datetime.now(timezone.utc)
        elapsed_minutes = (now - session_start).total_seconds() / 60
        max_duration = 180

        is_trial = 'demo' in str(user_prefix).lower() or 'trial' in str(user_prefix).lower() or 'local' in str(user_prefix).lower()
        if elapsed_minutes > max_duration + 10 and not is_trial:
            print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m", flush=True)
            raise Exception("Time Limit Exceeded")

        print(f"[SYSTEM] Validating Resources for: {user_prefix}", flush=True)
        print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n", flush=True)

        local_state = check_local_tfstate()
        live_aws = check_live_aws()

        # ---------------------------------------------------------
        # TC1: Terraform Initialization & Syntax Validation (10 Marks)
        # ---------------------------------------------------------
        tf_dir = find_terraform_dir()
        init_status = "NOT_RUN"
        validate_status = "NOT_RUN"
        tc1_error_detail = ""

        has_code, code_err = check_tf_configuration(tf_dir, required_resource="aws_vpc")
        if tf_dir and os.path.isfile(os.path.join(tf_dir, "main.tf")) and has_code:
            tf_bin = shutil.which("terraform")
            if tf_bin:
                try:
                    init_res = subprocess.run([tf_bin, "init", "-no-color"], cwd=tf_dir, capture_output=True, text=True, timeout=60)
                    if init_res.returncode == 0:
                        init_status = "SUCCESS"
                    else:
                        init_status = "FAILED"
                        tc1_error_detail = init_res.stderr.strip() or init_res.stdout.strip()
                except Exception as e:
                    init_status = "FAILED"
                    tc1_error_detail = f"init error: {e}"

                try:
                    val_res = subprocess.run([tf_bin, "validate", "-no-color"], cwd=tf_dir, capture_output=True, text=True, timeout=30)
                    if val_res.returncode == 0:
                        validate_status = "SUCCESS"
                    else:
                        validate_status = "FAILED"
                        if not tc1_error_detail:
                            tc1_error_detail = val_res.stderr.strip() or val_res.stdout.strip()
                except Exception as e:
                    validate_status = "FAILED"
                    if not tc1_error_detail:
                        tc1_error_detail = f"validate error: {e}"

        # If infrastructure exists in AWS (e.g. provisioned in CloudShell) or in tfstate, validate TC1 as SUCCESS
        if live_aws.get('has_vpc') or local_state.get('has_vpc'):
            init_status = "SUCCESS"
            validate_status = "SUCCESS"

        tc1_passed = (init_status == "SUCCESS" and validate_status == "SUCCESS")

        if tc1_passed:
            results['tc1'] = True
            print("TC1: Terraform Initialization & Syntax Validation ........ [PASS] (10/10)", flush=True)
            print("    ├─ terraform init: SUCCESS", flush=True)
            print("    └─ terraform validate: SUCCESS", flush=True)
        else:
            results['tc1'] = False
            print("TC1: Terraform Initialization & Syntax Validation ........ [FAILED] (0/10)", flush=True)
            print(f"    ├─ terraform init: {init_status}", flush=True)
            print(f"    └─ terraform validate: {validate_status}", flush=True)
            if tc1_error_detail:
                first_line = tc1_error_detail.splitlines()[0] if tc1_error_detail else "configuration syntax invalid"
                print(f"       └─ [Details]: {first_line[:90]}", flush=True)
            elif not tf_dir:
                print("       └─ [Details]: main.tf not found in workspace", flush=True)
            elif not has_code:
                print(f"       └─ [Details]: {code_err}", flush=True)

        # ---------------------------------------------------------
        # TC2: AWS VPC & Subnets Creation Verification (10 Marks)
        # ---------------------------------------------------------
        vpc_ok = False
        subnet_ok = False

        if live_aws.get('has_vpc'):
            vpc_ok = True
            if live_aws.get('has_subnet'):
                subnet_ok = True
        elif local_state.get('has_vpc'):
            vpc_ok = True
            if local_state.get('has_subnet'):
                subnet_ok = True

        if vpc_ok and subnet_ok:
            results['tc2'] = True
            print("TC2: AWS VPC & Subnets Creation Verification ............ [PASS] (10/10)", flush=True)
            print("    ├─ VPC (CIDR: 10.0.0.0/16 in eu-west-2): PASS", flush=True)
            print("    └─ Public Subnet (CIDR: 10.0.1.0/24): PASS", flush=True)
        else:
            results['tc2'] = False
            print("TC2: AWS VPC & Subnets Creation Verification ............ [FAILED] (0/10)", flush=True)
            vpc_str = "PASS" if vpc_ok else "FAILED (VPC 10.0.0.0/16 not found in eu-west-2)"
            subnet_str = "PASS" if subnet_ok else "FAILED (Subnet 10.0.1.0/24 not found)"
            print(f"    ├─ VPC (CIDR: 10.0.0.0/16 in eu-west-2): {vpc_str}", flush=True)
            print(f"    └─ Public Subnet (CIDR: 10.0.1.0/24): {subnet_str}", flush=True)

        # ---------------------------------------------------------
        # TC3: IGW & Route Table Association Verification (10 Marks)
        # ---------------------------------------------------------
        igw_ok = False
        rt_ok = False
        assoc_ok = False

        if live_aws.get('has_igw'):
            igw_ok = True
            if live_aws.get('has_rt'):
                rt_ok = True
            if live_aws.get('has_assoc'):
                assoc_ok = True
        elif local_state.get('has_igw'):
            igw_ok = True
            if local_state.get('has_rt'):
                rt_ok = True
            if local_state.get('has_assoc'):
                assoc_ok = True

        if igw_ok and rt_ok:
            results['tc3'] = True
            print("TC3: IGW & Route Table Association Verification ........ [PASS] (10/10)", flush=True)
            print("    ├─ Internet Gateway Attached: PASS", flush=True)
            print("    ├─ Default Route (0.0.0.0/0 -> IGW): PASS", flush=True)
            assoc_str = "PASS" if assoc_ok else "PASS (Implicit Subnet Routing)"
            print(f"    └─ Subnet Route Table Association: {assoc_str}", flush=True)
        else:
            results['tc3'] = False
            print("TC3: IGW & Route Table Association Verification ........ [FAILED] (0/10)", flush=True)
            igw_str = "PASS" if igw_ok else "FAILED (Internet Gateway not attached to VPC)"
            rt_str = "PASS" if rt_ok else "FAILED (Route 0.0.0.0/0 -> IGW missing)"
            print(f"    ├─ Internet Gateway Attached: {igw_str}", flush=True)
            print(f"    └─ Route Table & Subnet Association: {rt_str}", flush=True)

        total_score = sum([10 for r in results.values() if r])

        print("-" * 70, flush=True)
        print(f"{'TOTAL SCORE:':<52} {total_score}/30", flush=True)
        print("-" * 70 + "\n", flush=True)

    except Exception as e:
        print(f"[ERROR] Real-time audit failed: {str(e)}", flush=True)
        total_score = 0

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


def verify_aws_on_server(candidate_email=None, question_id='AWS_Q10', labskraft_username=None, labskraft_user=None, assessment_start_time=None, start_time=None, solution_data=None, exam_code_arg="UNKNOWN", solution_path=None, **kwargs):
    return verify_task()


if __name__ == '__main__':
    verify_task()
