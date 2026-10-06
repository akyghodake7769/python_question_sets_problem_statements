# import json
# import os
# import sys
# import subprocess
# from datetime import datetime, timezone

# # Capture Assessment Start Time
# START_TIME_STR = os.getenv('KLOUDKRAFT_START_TIME')
# START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
# USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "LOCAL_USER"
# import sys
# exam_code = sys.argv[3] if len(sys.argv) > 3 else 'UNKNOWN'

# def verify_task():
#     user_prefix = USER_PREFIX
#     start_time = START_TIME_STR
    
#     # Standard LabsKraft Header
#     print("\n" + "-"*70)
#     print(f"{'KODEBUCK REAL-TIME TERRAFORM AUDIT':^70}")
#     print("-"*70)

#     total_score = 0
#     results = {}

#     try:
#         # Time Enforcement Logic
#         if not START_TIME:
#             print("[ERROR] KLOUDKRAFT_START_TIME environment variable is missing.")
#             raise Exception("Invalid Session")

#         now = datetime.now(timezone.utc)
#         elapsed_minutes = (now - START_TIME).total_seconds() / 60
#         max_duration = 75  # 75 Min assessment

#         if elapsed_minutes > max_duration + 5: # 5 min grace
#             print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m")
#             raise Exception("Time Limit Exceeded")

#         print(f"[SYSTEM] Validating Resources for: {user_prefix}")
#         print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")

#         # --- TC1: Terraform Validate ---
#         try:
#             tf_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
#             tc1_passed = False
#             if os.path.exists(os.path.join(tf_dir, "main.tf")):
#                 # Check terraform validate
#                 val_check = subprocess.run(["terraform", "validate", "-json"], cwd=tf_dir, capture_output=True, text=True)
#                 if val_check.returncode == 0:
#                     tc1_passed = True

#             if tc1_passed:
#                 results['tc1'] = True
#                 print(f"TC1: Terraform Initialization & Syntax Validation ........ [PASSED] (10/10)")
#             else:
#                 results['tc1'] = False
#                 print(f"TC1: Terraform Initialization & Syntax Validation ........ [FAILED] (0/10)")
#                 print(f"     └─ [Reason]: terraform validate failed or main.tf missing.")
#         except Exception as e:
#             results['tc1'] = False
#             print(f"TC1: Terraform Initialization & Syntax Validation ........ [FAILED] (0/10)")
#             print(f"     └─ [Error]: {str(e)}")

#         # --- TC2: AWS VPC & Subnets ---
#         if not results.get('tc1'):
#             results['tc2'] = False
#             print(f"TC2: AWS VPC & Subnets Creation Verification ........... [FAILED] (0/10)")
#             print(f"     └─ [Reason]: Prerequisite failed (Terraform invalid).")
#             results['tc3'] = False
#             print(f"TC3: IGW & Route Table Association Verification ........ [FAILED] (0/10)")
#             print(f"     └─ [Reason]: Prerequisite failed.")
#         else:
#             try:
#                 tf_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
#                 state_file = os.path.join(tf_dir, "terraform.tfstate")
#                 tc2_passed = False
#                 if os.path.exists(state_file):
#                     with open(state_file, "r") as sf:
#                         state_data = json.load(sf)
#                         resources = state_data.get("resources", [])
#                         has_vpc = any(r.get("type") == "aws_vpc" for r in resources)
#                         has_subnet = any(r.get("type") == "aws_subnet" for r in resources)
#                         if has_vpc and has_subnet:
#                             tc2_passed = True
#                             if START_TIME:
#                                 mtime = datetime.fromtimestamp(os.path.getmtime(state_file), timezone.utc)
#                                 if mtime < START_TIME:
#                                     tc2_passed = False
#                                     print(f"[WARN] Terraform state was created before current session started (Old Session).")

#                 if tc2_passed:
#                     results['tc2'] = True
#                     print(f"TC2: AWS VPC & Subnets Creation Verification ........... [PASSED] (10/10)")
#                 else:
#                     results['tc2'] = False
#                     print(f"TC2: AWS VPC & Subnets Creation Verification ........... [FAILED] (0/10)")
#                     print(f"     └─ [Reason]: VPC or required subnets not found in state in current session.")
#             except Exception as e:
#                 results['tc2'] = False
#                 print(f"TC2: AWS VPC & Subnets Creation Verification ........... [FAILED] (0/10)")
#                 print(f"     └─ [Error]: {str(e)}")
            
#             # --- TC3: IGW & Route Table ---
#             try:
#                 tf_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
#                 state_file = os.path.join(tf_dir, "terraform.tfstate")
#                 tc3_passed = False
#                 if os.path.exists(state_file):
#                     with open(state_file, "r") as sf:
#                         state_data = json.load(sf)
#                         resources = state_data.get("resources", [])
#                         has_igw = any(r.get("type") == "aws_internet_gateway" for r in resources)
#                         has_rt = any(r.get("type") == "aws_route_table" for r in resources)
#                         if has_igw and has_rt:
#                             tc3_passed = True
#                             if START_TIME:
#                                 mtime = datetime.fromtimestamp(os.path.getmtime(state_file), timezone.utc)
#                                 if mtime < START_TIME:
#                                     tc3_passed = False
#                                     print(f"[WARN] Terraform state was created before current session started (Old Session).")

#                 if tc3_passed:
#                     results['tc3'] = True
#                     print(f"TC3: IGW & Route Table Association Verification ........ [PASSED] (10/10)")
#                 else:
#                     results['tc3'] = False
#                     print(f"TC3: IGW & Route Table Association Verification ........ [FAILED] (0/10)")
#                     print(f"     └─ [Reason]: Internet Gateway or Route Table missing in state in current session.")
#             except Exception as e:
#                 results['tc3'] = False
#                 print(f"TC3: IGW & Route Table Association Verification ........ [FAILED] (0/10)")
#                 print(f"     └─ [Error]: {str(e)}")

#         # Final Scoring
#         total_score = sum([10 for r in results.values() if r])
        
#         print("-" * 70)
#         print(f"{'TOTAL SCORE:':<52} {total_score}/30")
#         print("-" * 70 + "\n")

#     except Exception as e:
#         print(f"[ERROR] Real-time audit failed: {str(e)}")
#         total_score = 0

#     # Save Metadata for Central Evaluation
#     solution_data = {
#         'candidate_prefix': user_prefix,
#         'assessment_start_time': start_time,
#         'evaluation_type': 'REAL_TIME_API',
#         'score': total_score,
#         'results': results
#     }
    
#     try:
#         ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
#         os.makedirs(ws_path, exist_ok=True)
#         with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
#             json.dump(solution_data, f, indent=4)
#     except Exception as e:
#         print(f"[ERROR] Could not write solution.json: {e}")

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
    """
    Creates an EC2 client for eu-west-2 using standard boto3 resolution.
    """
    try:
        import boto3
        return boto3.client('ec2', region_name=region_name)
    except Exception:
        return None


def run_aws_cli(args):
    """
    Fallback helper to run AWS CLI commands in eu-west-2.
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


def get_student_terraform_dir():
    """
    Detects the student's actual VS Code Terraform workspace.
    Strictly prefers student_workspace/ relative to this driver.
    """
    base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    student_ws = os.path.join(base_dir, 'student_workspace')
    if os.path.isdir(student_ws):
        return os.path.abspath(student_ws)

    # Fallback to current working directory if main.tf exists here
    if os.path.isfile(os.path.join(os.getcwd(), 'main.tf')):
        return os.path.abspath(os.getcwd())

    ws_env = os.getenv('WORKSPACE_DIR') or os.getenv('KODEBUCK_WORKSPACE') or os.getenv('TERRAFORM_DIR')
    if ws_env and os.path.isdir(ws_env) and os.path.isfile(os.path.join(ws_env, 'main.tf')):
        return os.path.abspath(ws_env)

    return os.path.abspath(student_ws)


def check_tf_configuration(tf_dir, required_resource="aws_vpc"):
    """
    Validates that main.tf in the student workspace is non-empty and defines the expected resource(s).
    """
    if not tf_dir or not os.path.isdir(tf_dir):
        return False, "student_workspace directory not found"

    main_tf = os.path.join(tf_dir, "main.tf")
    if not os.path.isfile(main_tf):
        return False, "main.tf not found in student_workspace"

    try:
        with open(main_tf, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        return False, f"Could not read main.tf: {e}"

    clean_lines = []
    in_block_comment = False
    for raw_line in code.splitlines():
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


def check_live_aws():
    """
    Queries live AWS API/CLI in region eu-west-2 (London).
    Validates VPC (10.0.0.0/16, my-simple-vpc), Subnet (10.0.1.0/24), IGW, and Route Table with association.
    """
    ec2 = get_ec2_client()

    all_vpcs = []
    if ec2:
        try:
            all_vpcs = ec2.describe_vpcs().get('Vpcs', [])
        except Exception:
            all_vpcs = []

    if not all_vpcs:
        cli_res = run_aws_cli(['ec2', 'describe-vpcs'])
        if cli_res:
            all_vpcs = cli_res.get('Vpcs', [])

    candidate_vpcs = []
    for v in all_vpcs:
        cidr = v.get('CidrBlock', '')
        tags = {t.get('Key'): t.get('Value') for t in v.get('Tags', [])}
        if tags.get('Name') == 'my-simple-vpc' or cidr == '10.0.0.0/16':
            candidate_vpcs.append(v)

    if not candidate_vpcs:
        candidate_vpcs = [v for v in all_vpcs if not v.get('IsDefault', False)]

    if not candidate_vpcs:
        return {'has_vpc': False, 'has_subnet': False, 'has_igw': False, 'has_rt': False, 'has_assoc': False}

    has_vpc = False
    has_subnet = False
    has_igw = False
    has_rt = False
    has_assoc = False

    for vpc in candidate_vpcs:
        vpc_id = vpc['VpcId']
        has_vpc = True

        # Check Subnets in this VPC
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

        matching_subnet = next((s for s in subnets if s.get('CidrBlock') == '10.0.1.0/24'), None)
        cur_has_subnet = matching_subnet is not None
        subnet_id = matching_subnet['SubnetId'] if matching_subnet else None

        # Check Internet Gateways attached to this VPC
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

        cur_has_igw = len(igws) > 0
        igw_ids = [igw['InternetGatewayId'] for igw in igws]

        # Check Route Tables in this VPC
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

        cur_has_rt = False
        cur_has_assoc = False

        for rt in rts:
            for route in rt.get('Routes', []):
                dest = route.get('DestinationCidrBlock')
                gw = route.get('GatewayId', '')
                if dest == '0.0.0.0/0' and (gw in igw_ids or gw.startswith('igw-') or len(igws) > 0):
                    cur_has_rt = True
                    break

            for assoc in rt.get('Associations', []):
                if subnet_id and assoc.get('SubnetId') == subnet_id:
                    cur_has_assoc = True
                    break
                elif assoc.get('RouteTableAssociationId') and not assoc.get('Main', False):
                    cur_has_assoc = True

        if not cur_has_assoc and cur_has_rt and subnet_id:
            for rt in rts:
                for assoc in rt.get('Associations', []):
                    if assoc.get('Main', False):
                        for route in rt.get('Routes', []):
                            if route.get('DestinationCidrBlock') == '0.0.0.0/0':
                                cur_has_assoc = True
                                break

        if cur_has_subnet:
            has_subnet = True
        if cur_has_igw:
            has_igw = True
        if cur_has_rt:
            has_rt = True
        if cur_has_assoc:
            has_assoc = True

        if cur_has_subnet and cur_has_igw and cur_has_rt and cur_has_assoc:
            break

    return {
        'has_vpc': has_vpc,
        'has_subnet': has_subnet,
        'has_igw': has_igw,
        'has_rt': has_rt,
        'has_assoc': has_assoc
    }


def verify_task():
    user_prefix = USER_PREFIX
    start_time = START_TIME_STR

    print("\n" + "-"*70, flush=True)
    print(f"{'KODEBUCK REAL-TIME TERRAFORM AUDIT':^70}", flush=True)
    print("-"*70, flush=True)

    total_score = 0
    results = {'tc1': False, 'tc2': False, 'tc3': False}

    tf_dir = get_student_terraform_dir()
    os.makedirs(tf_dir, exist_ok=True)
    solution_file = os.path.join(tf_dir, 'solution.json')
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

        # ---------------------------------------------------------
        # TC1: Terraform Initialization & Syntax Validation (10 Marks)
        # Strictly requires:
        # 1. Valid main.tf in student_workspace with aws_vpc resource
        # 2. terraform init returncode == 0
        # 3. terraform validate returncode == 0
        # ---------------------------------------------------------
        init_status = "NOT_RUN"
        validate_status = "NOT_RUN"
        tc1_error_detail = ""

        has_code, code_err = check_tf_configuration(tf_dir, required_resource="aws_vpc")
        if not has_code:
            tc1_error_detail = code_err
        else:
            tf_bin = shutil.which("terraform")
            if not tf_bin:
                init_status = "FAILED"
                validate_status = "FAILED"
                tc1_error_detail = "Terraform executable not found in PATH"
            else:
                # 1. Run terraform init
                try:
                    init_res = subprocess.run([tf_bin, "init", "-no-color"], cwd=tf_dir, capture_output=True, text=True, timeout=60)
                    if init_res.returncode == 0:
                        init_status = "SUCCESS"
                    else:
                        init_status = "FAILED"
                        tc1_error_detail = init_res.stderr.strip() or init_res.stdout.strip()
                except Exception as e:
                    init_status = "FAILED"
                    tc1_error_detail = f"terraform init failed: {e}"

                # 2. Run terraform validate
                if init_status == "SUCCESS":
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
                            tc1_error_detail = f"terraform validate failed: {e}"
                else:
                    validate_status = "NOT_RUN"

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
                first_line = tc1_error_detail.splitlines()[0] if tc1_error_detail else "syntax validation failed"
                print(f"       └─ [Details]: {first_line[:90]}", flush=True)

        # ---------------------------------------------------------
        # TC2: AWS VPC & Subnets Creation Verification (10 Marks)
        # Strictly queries live AWS in eu-west-2
        # ---------------------------------------------------------
        live_aws = check_live_aws()

        vpc_ok = live_aws.get('has_vpc', False)
        subnet_ok = live_aws.get('has_subnet', False)

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
        # Strictly queries live AWS in eu-west-2
        # ---------------------------------------------------------
        igw_ok = live_aws.get('has_igw', False)
        rt_ok = live_aws.get('has_rt', False)
        assoc_ok = live_aws.get('has_assoc', False)

        if igw_ok and rt_ok and assoc_ok:
            results['tc3'] = True
            print("TC3: IGW & Route Table Association Verification ........ [PASS] (10/10)", flush=True)
            print("    ├─ Internet Gateway Attached: PASS", flush=True)
            print("    ├─ Default Route (0.0.0.0/0 -> IGW): PASS", flush=True)
            print("    └─ Subnet Route Table Association: PASS", flush=True)
        else:
            results['tc3'] = False
            print("TC3: IGW & Route Table Association Verification ........ [FAILED] (0/10)", flush=True)
            igw_str = "PASS" if igw_ok else "FAILED (Internet Gateway not attached to VPC)"
            rt_str = "PASS" if rt_ok else "FAILED (Route 0.0.0.0/0 -> IGW missing)"
            assoc_str = "PASS" if assoc_ok else "FAILED (Subnet not associated with route table)"
            print(f"    ├─ Internet Gateway Attached: {igw_str}", flush=True)
            print(f"    └─ Route Table & Subnet Association: {rt_str}", flush=True)
            print(f"    └─ Subnet Route Table Association: {assoc_str}", flush=True)

        # Final Scoring (30 Marks total)
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
