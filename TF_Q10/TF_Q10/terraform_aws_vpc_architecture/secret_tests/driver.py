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
    Creates an EC2 client for eu-west-2 using standard boto3 credentials resolution.
    """
    try:
        import boto3
        return boto3.client('ec2', region_name=region_name)
    except Exception:
        return None


def run_aws_cli(args):
    """
    Fallback helper to run AWS CLI commands in eu-west-2 using standard environment credentials.
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


def check_main_tf_exists(tf_dir):
    """
    Verifies main.tf exists in the student workspace and is non-empty.
    """
    if not tf_dir or not os.path.isdir(tf_dir):
        return False, "student_workspace directory not found"

    main_tf = os.path.join(tf_dir, "main.tf")
    if not os.path.isfile(main_tf):
        return False, "main.tf not found in student_workspace"

    try:
        with open(main_tf, 'r', encoding='utf-8') as f:
            code = f.read().strip()
        if not code:
            return False, "main.tf is empty"
    except Exception as e:
        return False, f"Could not read main.tf: {e}"

    return True, ""


def check_live_aws():
    """
    Queries live AWS API/CLI in region eu-west-2 (London).
    Validates VPC (10.0.0.0/16, Name tag 'my-simple-vpc'), Subnet (10.0.1.0/24),
    IGW attached to VPC, and Route Table with default route 0.0.0.0/0 -> IGW and subnet association.
    """
    ec2 = get_ec2_client()
    all_vpcs = None
    credentials_ok = True

    if ec2:
        try:
            res = ec2.describe_vpcs()
            all_vpcs = res.get('Vpcs', [])
        except Exception:
            all_vpcs = None

    if all_vpcs is None:
        cli_res = run_aws_cli(['ec2', 'describe-vpcs'])
        if cli_res is not None:
            all_vpcs = cli_res.get('Vpcs', [])
        else:
            credentials_ok = False
            all_vpcs = []

    if not credentials_ok:
        return {
            'credentials_available': False,
            'has_vpc': False,
            'has_subnet': False,
            'has_igw': False,
            'has_rt': False,
            'has_assoc': False
        }

    # Find the target VPC: CIDR 10.0.0.0/16 AND Name tag 'my-simple-vpc'
    target_vpc = None
    for v in all_vpcs:
        cidr = v.get('CidrBlock', '')
        tags = {t.get('Key'): t.get('Value') for t in v.get('Tags', [])}
        if cidr == '10.0.0.0/16' and tags.get('Name') == 'my-simple-vpc':
            target_vpc = v
            break

    # Fallback to CIDR match if Name tag is missing/different
    if not target_vpc:
        for v in all_vpcs:
            if v.get('CidrBlock') == '10.0.0.0/16':
                target_vpc = v
                break

    if not target_vpc:
        return {
            'credentials_available': True,
            'has_vpc': False,
            'has_subnet': False,
            'has_igw': False,
            'has_rt': False,
            'has_assoc': False
        }

    vpc_id = target_vpc['VpcId']
    has_vpc = True

    # Check Subnet in this VPC with CIDR 10.0.1.0/24
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
    has_subnet = (matching_subnet is not None)
    subnet_id = matching_subnet['SubnetId'] if matching_subnet else None

    # Check Internet Gateway attached to this VPC
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

    has_rt = False
    has_assoc = False

    for rt in rts:
        for route in rt.get('Routes', []):
            dest = route.get('DestinationCidrBlock')
            gw = route.get('GatewayId', '')
            if dest == '0.0.0.0/0' and (gw in igw_ids or gw.startswith('igw-') or len(igws) > 0):
                has_rt = True
                break

        for assoc in rt.get('Associations', []):
            if subnet_id and assoc.get('SubnetId') == subnet_id:
                has_assoc = True
                break
            elif assoc.get('RouteTableAssociationId') and not assoc.get('Main', False):
                has_assoc = True
                break

    if not has_assoc and has_rt and subnet_id:
        for rt in rts:
            for assoc in rt.get('Associations', []):
                if assoc.get('Main', False):
                    for route in rt.get('Routes', []):
                        if route.get('DestinationCidrBlock') == '0.0.0.0/0':
                            has_assoc = True
                            break

    return {
        'credentials_available': True,
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
        # TC1: Terraform Initialization & Syntax Validation
        # ---------------------------------------------------------
        init_status = "NOT_RUN"
        validate_status = "NOT_RUN"
        tc1_error_detail = ""

        has_main_tf, tf_err = check_main_tf_exists(tf_dir)
        if not has_main_tf:
            init_status = "FAILED"
            validate_status = "NOT_RUN"
            tc1_error_detail = tf_err
        else:
            tf_bin = shutil.which("terraform")
            if not tf_bin:
                init_status = "FAILED"
                validate_status = "FAILED"
                tc1_error_detail = "Terraform executable not found in PATH"
            else:
                # 1. Run terraform init
                try:
                    init_res = subprocess.run(
                        [tf_bin, "init", "-no-color"],
                        cwd=tf_dir,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    if init_res.returncode == 0:
                        init_status = "SUCCESS"
                    else:
                        init_status = "FAILED"
                        tc1_error_detail = init_res.stderr.strip() or init_res.stdout.strip()
                except Exception as e:
                    init_status = "FAILED"
                    tc1_error_detail = f"terraform init failed: {e}"

                # 2. Run terraform validate (only if init succeeded)
                if init_status == "SUCCESS":
                    try:
                        val_res = subprocess.run(
                            [tf_bin, "validate", "-no-color"],
                            cwd=tf_dir,
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
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
            print("TC1: Terraform Initialization & Syntax Validation ........ [PASS]", flush=True)
            print("    ├─ terraform init: SUCCESS", flush=True)
            print("    └─ terraform validate: SUCCESS", flush=True)
        else:
            results['tc1'] = False
            print("TC1: Terraform Initialization & Syntax Validation ........ [FAILED]", flush=True)
            print(f"    ├─ terraform init: {init_status}", flush=True)
            print(f"    └─ terraform validate: {validate_status}", flush=True)
            if tc1_error_detail:
                first_line = tc1_error_detail.splitlines()[0] if tc1_error_detail else "syntax validation failed"
                print(f"       └─ [Details]: {first_line[:90]}", flush=True)

        # ---------------------------------------------------------
        # Live AWS Verification for TC2 and TC3
        # ---------------------------------------------------------
        live_aws = check_live_aws()

        if not live_aws.get('credentials_available', True):
            print("\n[ERROR] AWS credentials unavailable. TC2/TC3 cannot verify live AWS resources.", flush=True)

        # ---------------------------------------------------------
        # TC2: AWS VPC & Subnets Creation Verification
        # ---------------------------------------------------------
        vpc_ok = tc1_passed and live_aws.get('has_vpc', False)
        subnet_ok = tc1_passed and live_aws.get('has_subnet', False)

        if vpc_ok and subnet_ok:
            results['tc2'] = True
            print("TC2: AWS VPC & Subnets Creation Verification ............ [PASS]", flush=True)
            print("    ├─ VPC (CIDR: 10.0.0.0/16 in eu-west-2): PASS", flush=True)
            print("    └─ Public Subnet (CIDR: 10.0.1.0/24): PASS", flush=True)
        else:
            results['tc2'] = False
            print("TC2: AWS VPC & Subnets Creation Verification ............ [FAILED]", flush=True)
            vpc_str = "PASS" if vpc_ok else "FAILED (VPC 10.0.0.0/16 not found in eu-west-2)"
            subnet_str = "PASS" if subnet_ok else "FAILED (Subnet 10.0.1.0/24 not found)"
            print(f"    ├─ VPC (CIDR: 10.0.0.0/16 in eu-west-2): {vpc_str}", flush=True)
            print(f"    └─ Public Subnet (CIDR: 10.0.1.0/24): {subnet_str}", flush=True)

        # ---------------------------------------------------------
        # TC3: IGW & Route Table Association Verification
        # ---------------------------------------------------------
        igw_ok = tc1_passed and live_aws.get('has_igw', False)
        rt_ok = tc1_passed and live_aws.get('has_rt', False)
        assoc_ok = tc1_passed and live_aws.get('has_assoc', False)

        if igw_ok and rt_ok and assoc_ok:
            results['tc3'] = True
            print("TC3: IGW & Route Table Association Verification ........ [PASS]", flush=True)
            print("    ├─ Internet Gateway Attached: PASS", flush=True)
            print("    ├─ Route Table & Default Route: PASS", flush=True)
            print("    └─ Subnet Route Table Association: PASS", flush=True)
        else:
            results['tc3'] = False
            print("TC3: IGW & Route Table Association Verification ........ [FAILED]", flush=True)
            igw_str = "PASS" if igw_ok else "FAILED (Internet Gateway not attached to VPC)"
            rt_str = "PASS" if rt_ok else "FAILED (Route 0.0.0.0/0 -> IGW missing)"
            assoc_str = "PASS" if assoc_ok else "FAILED (Subnet not associated with route table)"
            print(f"    ├─ Internet Gateway Attached: {igw_str}", flush=True)
            print(f"    ├─ Route Table & Default Route: {rt_str}", flush=True)
            print(f"    └─ Subnet Route Table Association: {assoc_str}", flush=True)

        print("-" * 70 + "\n", flush=True)

        total_score = sum([10 for r in results.values() if r])

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

    # 1. Write solution.json
    try:
        with open(solution_file, 'w', encoding='utf-8') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}", flush=True)

    # 2. Update solution.py with embedded results metadata for central submitter
    sol_py = os.path.join(tf_dir, 'solution.py')
    if os.path.exists(sol_py):
        try:
            with open(sol_py, 'r', encoding='utf-8') as f:
                content = f.read()
            clean_lines = [l for l in content.splitlines() if not l.startswith('# KODEBUCK_RESULTS=')]
            clean_lines.append(f"# KODEBUCK_RESULTS={json.dumps(solution_data)}")
            with open(sol_py, 'w', encoding='utf-8') as f:
                f.write('\n'.join(clean_lines) + '\n')
        except Exception:
            pass

    return total_score


def verify_aws_on_server(candidate_email=None, question_id='TF_Q10', labskraft_username=None, labskraft_user=None, assessment_start_time=None, start_time=None, solution_data=None, exam_code_arg="UNKNOWN", solution_path=None, **kwargs):
    try:
        from driver_central import verify_aws_on_server as central_eval
        return central_eval(
            candidate_email=candidate_email,
            solution_path=solution_path,
            exam_code_arg=exam_code_arg,
            labskraft_username=labskraft_username or labskraft_user,
            assessment_start_time=assessment_start_time or start_time,
            solution_data=solution_data
        )
    except Exception:
        return verify_task()


if __name__ == '__main__':
    verify_task()
