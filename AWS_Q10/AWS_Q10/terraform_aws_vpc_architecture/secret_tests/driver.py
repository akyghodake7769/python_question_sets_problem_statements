# import json
# import os
# import sys
# import subprocess
# from datetime import datetime, timezone

# # Capture Assessment Start Time
# START_TIME_STR = os.getenv('KLOUDKRAFT_START_TIME')
# START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
# USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "LOCAL_USER"

# def verify_task():
#     user_prefix = USER_PREFIX
#     start_time = START_TIME_STR
    
#     # Standard LabsKraft Header
#     print("\n" + "-"*70)
#     print(f"{'KODEARENA REAL-TIME TERRAFORM AUDIT':^70}")
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
from datetime import datetime, timezone

try:
    import boto3
except ImportError:
    boto3 = None

# Capture Assessment Start Time
START_TIME_STR = os.getenv('KLOUDKRAFT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "LOCAL_USER"

def check_live_aws():
    """
    Check if VPC, Subnet, IGW, and Route Table exist in the AWS account.
    Scans common regions, prioritizing the configured default region and eu-west-1.
    """
    if boto3 is None:
        return None

    regions = []
    default_reg = os.getenv('AWS_DEFAULT_REGION') or os.getenv('AWS_REGION')
    if default_reg:
        regions.append(default_reg)
    for r in ['eu-west-1', 'eu-west-2', 'eu-west-3', 'us-east-1', 'us-east-2', 'us-west-2', 'ap-south-1']:
        if r not in regions:
            regions.append(r)

    # Try to dynamically list regions if credentials allow
    try:
        sts = boto3.client('sts')
        sts.get_caller_identity()
        ec2_temp = boto3.client('ec2', region_name=regions[0])
        all_regs = [reg['RegionName'] for reg in ec2_temp.describe_regions().get('Regions', [])]
        for r in all_regs:
            if r not in regions:
                regions.append(r)
    except Exception:
        pass

    for r in regions:
        try:
            ec2 = boto3.client('ec2', region_name=r)
            vpcs_resp = ec2.describe_vpcs()
            vpcs = vpcs_resp.get('Vpcs', [])
            if not vpcs:
                continue

            matching_vpc = None
            # Priority 1: Match both Name tag 'my-simple-vpc' and CIDR 10.0.0.0/16
            for v in vpcs:
                tags = {t.get('Key'): t.get('Value') for t in v.get('Tags', [])}
                name_tag = tags.get('Name', '').lower()
                cidr = v.get('CidrBlock', '')
                if ('my-simple-vpc' in name_tag or 'simple-vpc' in name_tag) and cidr == '10.0.0.0/16':
                    matching_vpc = v
                    break

            # Priority 2: Match Name tag 'my-simple-vpc'
            if not matching_vpc:
                for v in vpcs:
                    tags = {t.get('Key'): t.get('Value') for t in v.get('Tags', [])}
                    name_tag = tags.get('Name', '').lower()
                    if 'my-simple-vpc' in name_tag:
                        matching_vpc = v
                        break

            # Priority 3: Match CIDR 10.0.0.0/16 and not default VPC
            if not matching_vpc:
                for v in vpcs:
                    if v.get('CidrBlock') == '10.0.0.0/16' and not v.get('IsDefault', False):
                        matching_vpc = v
                        break

            if not matching_vpc:
                continue

            vpc_id = matching_vpc['VpcId']

            # Check Subnets in this VPC (CIDR 10.0.1.0/24)
            subnets_resp = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            subnets = subnets_resp.get('Subnets', [])
            has_subnet = any(s.get('CidrBlock') == '10.0.1.0/24' for s in subnets)

            # Check Internet Gateway attached to this VPC
            igw_resp = ec2.describe_internet_gateways(Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}])
            igws = igw_resp.get('InternetGateways', [])
            has_igw = len(igws) > 0
            igw_ids = [igw['InternetGatewayId'] for igw in igws]

            # Check Route Tables in this VPC
            rt_resp = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            rts = rt_resp.get('RouteTables', [])
            has_rt = False

            for rt in rts:
                routes = rt.get('Routes', [])
                for route in routes:
                    dest = route.get('DestinationCidrBlock')
                    gw = route.get('GatewayId', '')
                    if dest == '0.0.0.0/0' and (gw in igw_ids or gw.startswith('igw-')):
                        has_rt = True
                        break
                if has_rt:
                    break

            return {
                'region': r,
                'vpc_id': vpc_id,
                'has_vpc': True,
                'has_subnet': has_subnet,
                'has_igw': has_igw,
                'has_rt': has_rt
            }
        except Exception:
            continue

    return None

def check_local_workspace():
    """
    Check student workspace or lab folders for main.tf and terraform.tfstate.
    """
    candidate_dirs = [
        os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace')),
        os.path.expanduser('~/student_workspace'),
        os.path.expanduser('~/terraform-vpc-lab'),
        os.path.expanduser('~')
    ]

    tf_dir = None
    has_valid_main = False
    has_vpc_state = False
    has_subnet_state = False
    has_igw_state = False
    has_rt_state = False

    for d in candidate_dirs:
        main_path = os.path.join(d, "main.tf")
        if os.path.exists(main_path):
            tf_dir = d
            val_check = subprocess.run(["terraform", "validate", "-json"], cwd=d, capture_output=True, text=True)
            if val_check.returncode == 0:
                has_valid_main = True
            break

    for d in candidate_dirs:
        state_file = os.path.join(d, "terraform.tfstate")
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as sf:
                    state_data = json.load(sf)
                    resources = state_data.get("resources", [])
                    has_vpc_state = any(r.get("type") == "aws_vpc" for r in resources)
                    has_subnet_state = any(r.get("type") == "aws_subnet" for r in resources)
                    has_igw_state = any(r.get("type") == "aws_internet_gateway" for r in resources)
                    has_rt_state = any(r.get("type") == "aws_route_table" for r in resources)
                    break
            except Exception:
                pass

    return {
        'has_valid_main': has_valid_main,
        'has_vpc_state': has_vpc_state,
        'has_subnet_state': has_subnet_state,
        'has_igw_state': has_igw_state,
        'has_rt_state': has_rt_state
    }

def verify_task():
    user_prefix = USER_PREFIX
    start_time = START_TIME_STR
    
    # Standard LabsKraft Header
    print("\n" + "-"*70)
    print(f"{'KODEARENA REAL-TIME TERRAFORM AUDIT':^70}")
    print("-"*70)

    total_score = 0
    results = {}

    try:
        now = datetime.now(timezone.utc)
        if START_TIME:
            elapsed_minutes = (now - START_TIME).total_seconds() / 60
            max_duration = 75  # 75 Min assessment
            if elapsed_minutes > max_duration + 5: # 5 min grace
                print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m")
                raise Exception("Time Limit Exceeded")
            print(f"[SYSTEM] Validating Resources for: {user_prefix}")
            print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")
        else:
            print(f"[SYSTEM] Validating Resources for: {user_prefix}\n")

        # Discover live AWS resources
        live_aws = check_live_aws()
        local_ws = check_local_workspace()

        # --- TC1: Terraform Validate ---
        tc1_passed = False
        if local_ws['has_valid_main']:
            tc1_passed = True
        elif live_aws and live_aws.get('has_vpc'):
            # If the VPC exists live in AWS, Terraform was successfully initialized, validated, and applied in CloudShell
            tc1_passed = True
        elif local_ws['has_vpc_state']:
            tc1_passed = True

        if tc1_passed:
            results['tc1'] = True
            print(f"TC1: Terraform Initialization & Syntax Validation ........ [PASSED] (10/10)")
        else:
            results['tc1'] = False
            print(f"TC1: Terraform Initialization & Syntax Validation ........ [FAILED] (0/10)")
            print(f"     └─ [Reason]: terraform validate failed, main.tf missing, and VPC not found in AWS.")

        # --- TC2: AWS VPC & Subnets ---
        tc2_passed = False
        if live_aws and live_aws.get('has_vpc') and live_aws.get('has_subnet'):
            tc2_passed = True
        elif local_ws['has_vpc_state'] and local_ws['has_subnet_state']:
            tc2_passed = True

        if tc2_passed:
            results['tc2'] = True
            print(f"TC2: AWS VPC & Subnets Creation Verification ........... [PASSED] (10/10)")
        else:
            results['tc2'] = False
            print(f"TC2: AWS VPC & Subnets Creation Verification ........... [FAILED] (0/10)")
            print(f"     └─ [Reason]: VPC (10.0.0.0/16) or Subnet (10.0.1.0/24) not found in AWS or state.")

        # --- TC3: IGW & Route Table ---
        tc3_passed = False
        if live_aws and live_aws.get('has_igw') and live_aws.get('has_rt'):
            tc3_passed = True
        elif local_ws['has_igw_state'] and local_ws['has_rt_state']:
            tc3_passed = True

        if tc3_passed:
            results['tc3'] = True
            print(f"TC3: IGW & Route Table Association Verification ........ [PASSED] (10/10)")
        else:
            results['tc3'] = False
            print(f"TC3: IGW & Route Table Association Verification ........ [FAILED] (0/10)")
            print(f"     └─ [Reason]: Internet Gateway or Route Table (0.0.0.0/0 -> IGW) not found in AWS or state.")

        # Final Scoring
        total_score = sum([10 for r in results.values() if r])
        
        print("-" * 70)
        print(f"{'TOTAL SCORE:':<52} {total_score}/30")
        print("-" * 70 + "\n")

    except Exception as e:
        print(f"[ERROR] Real-time audit failed: {str(e)}")
        total_score = 0

    # Save Metadata for Central Evaluation
    solution_data = {
        'candidate_prefix': user_prefix,
        'assessment_start_time': start_time,
        'evaluation_type': 'REAL_TIME_API',
        'score': total_score,
        'results': results
    }
    
    try:
        ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
        os.makedirs(ws_path, exist_ok=True)
        with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}")

if __name__ == '__main__':
    verify_task()
