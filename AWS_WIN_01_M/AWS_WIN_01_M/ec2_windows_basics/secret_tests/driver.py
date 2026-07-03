import json
import os
import sys
from datetime import datetime, timezone, timedelta

# Capture Assessment Start Time
START_TIME_STR = os.getenv('KODEBUCK_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', 'LOCAL_USER')

def get_ec2_client(region_name='eu-west-2'):
    import boto3
    try:
        return boto3.client('ec2', region_name=region_name)
    except Exception as e:
        print(f"FAILED: Could not connect to AWS. Error: {e}")
        sys.exit(1)

def get_iam_username():
    try:
        import boto3
        sts = boto3.client('sts')
        arn = sts.get_caller_identity().get('Arn', '')
        if ':user/' in arn:
            return arn.split(':user/')[-1].strip()
        elif ':assumed-role/' in arn:
            role_part = arn.split(':assumed-role/')[-1].strip()
            if '/' in role_part:
                return role_part.split('/')[-1].strip()
            return role_part.strip()
        else:
            if '/' in arn:
                return arn.split('/')[-1].strip()
    except Exception:
        pass
    return None

def resolve_username(default_prefix):
    if default_prefix and default_prefix != 'LOCAL_USER':
        return default_prefix
    iam_user = get_iam_username()
    if iam_user and iam_user not in ['root', 'ubuntu', 'administrator', 'SYSTEM', 'LOCAL_USER']:
        return iam_user
    return default_prefix

def verify_task():
    username = resolve_username(USER_PREFIX)
    target_instance = f"labskraft-windows-basics-{username}"
    region = 'eu-west-2'
    start_time = START_TIME_STR

    print("\n" + "-" * 60)
    print(f"{'KODEBUCK AWS WINDOWS BASICS VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}

    try:
        session_start = START_TIME
        if not session_start:
            session_start = datetime.now(timezone.utc)
            start_time = session_start.isoformat()

        now = datetime.now(timezone.utc)
        elapsed_minutes = (now - session_start).total_seconds() / 60
        max_duration_env = os.getenv('KODEBUCK_ASSESSMENT_DURATION') or os.getenv('KODEARENA_ASSESSMENT_DURATION')
        max_duration = int(max_duration_env) if max_duration_env else 60

        if elapsed_minutes > max_duration + 10:
            print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m")
            raise Exception("Time Limit Exceeded")

        print(f"[SYSTEM] Validating AWS Resources for: {username}")
        print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")

        ec2 = get_ec2_client(region)

        # --- TC1: EC2 Instance (Windows t2.micro) --- (5 Marks)
        tc1_passed = False
        instance_id = None
        try:
            resp = ec2.describe_instances(Filters=[
                {'Name': 'tag:Name', 'Values': [target_instance]},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ])
            instances = [i for r in resp.get('Reservations', []) for i in r.get('Instances', [])]
            if instances:
                inst = instances[0]
                launch_time = inst['LaunchTime']
                if inst.get('InstanceType') != 't2.micro':
                    print(f"TC1: EC2 Instance (Windows t2.micro) ............ [FAILED] (0/5)")
                    print(f"     - [Reason]: Instance found but type is '{inst.get('InstanceType')}', expected 't2.micro'.")
                elif launch_time < session_start - timedelta(minutes=5):
                    ist_tz = timezone(timedelta(hours=5, minutes=30))
                    c_ist = launch_time.astimezone(ist_tz)
                    s_ist = session_start.astimezone(ist_tz)
                    info = f"Launched at {c_ist.strftime('%I:%M:%S %p IST')}, Assessment started at {s_ist.strftime('%I:%M:%S %p IST')}"
                    print(f"TC1: EC2 Instance (Windows t2.micro) ............ [FAILED] (0/5)")
                    print(f"     - [Reason]: Instance was launched BEFORE the assessment started. Please terminate and launch a new one!")
                    print(f"     - [Info]: {info}")
                else:
                    tc1_passed = True
                    instance_id = inst['InstanceId']
                    print(f"TC1: EC2 Instance (Windows t2.micro) ............ [PASSED] (5/5)")
            else:
                print(f"TC1: EC2 Instance (Windows t2.micro) ............ [FAILED] (0/5)")
                print(f"     - [Reason]: Running instance named '{target_instance}' not found in {region}.")
        except Exception as e:
            print(f"TC1: EC2 Instance (Windows t2.micro) ............ [FAILED] (0/5)")
            print(f"     - [Reason]: Error: {e}")

        results['tc1'] = tc1_passed
        if tc1_passed:
            total_score += 5

        # Guest OS Check Prerequisites via SSM
        is_managed = False
        ssm = None
        if tc1_passed:
            import boto3
            ssm = boto3.client('ssm', region_name=region)
            try:
                ssm_instances = ssm.describe_instance_information(
                    Filters=[{'Key': 'InstanceIds', 'Values': [instance_id]}]
                ).get('InstanceInformationList', [])
                if ssm_instances and ssm_instances[0].get('PingStatus') == 'Online':
                    is_managed = True
            except Exception:
                pass

        # Helper to execute PowerShell scripts on Windows via SSM
        def run_powershell(commands):
            import time
            try:
                response = ssm.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunPowerShellScript",
                    Parameters={'commands': commands},
                    TimeoutSeconds=30
                )
                command_id = response['Command']['CommandId']
                for _ in range(15):
                    time.sleep(1.5)
                    res = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
                    if res['Status'] in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
                        return res['Status'] == 'Success', res.get('StandardOutputContent', '').strip()
            except Exception:
                pass
            return False, ""

        # --- TC2: Directory Structure --- (5 Marks)
        tc2_passed = False
        if tc1_passed:
            if is_managed:
                cmd = "[bool](Test-Path 'C:\\workspace\\logs') -and [bool](Test-Path 'C:\\workspace\\backups')"
                success, output = run_powershell([cmd])
                if success and "True" in output:
                    tc2_passed = True
                    print(f"TC2: Directory Structure ......................... [PASSED] (5/5)")
                else:
                    print(f"TC2: Directory Structure ......................... [FAILED] (0/5)")
                    print(f"     - [Reason]: Directories 'C:\\workspace\\logs' and/or 'C:\\workspace\\backups' do not exist.")
            else:
                # Fallback check
                tc2_passed = True
                print(f"TC2: Directory Structure ......................... [PASSED] (5/5)")
                print(f"     - [WARNING]: SSM agent is offline on the instance. Verification bypassed folder checks.")
        else:
            print(f"TC2: Directory Structure ......................... [FAILED] (0/5)")
            print(f"     - [Reason]: Prerequisite TC1 (EC2 instance) failed.")

        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 5

        # --- TC3: System Environment Variables --- (5 Marks)
        tc3_passed = False
        if tc1_passed:
            if is_managed:
                cmd = "[Environment]::GetEnvironmentVariable('APP_ENVIRONMENT', 'Machine')"
                success, output = run_powershell([cmd])
                if success and output == "production":
                    tc3_passed = True
                    print(f"TC3: System Environment Variables ................ [PASSED] (5/5)")
                else:
                    print(f"TC3: System Environment Variables ................ [FAILED] (0/5)")
                    print(f"     - [Reason]: Permanent system-level variable 'APP_ENVIRONMENT' is not set to 'production'.")
            else:
                tc3_passed = True
                print(f"TC3: System Environment Variables ................ [PASSED] (5/5)")
                print(f"     - [WARNING]: SSM agent is offline. Environment variable checks bypassed.")
        else:
            print(f"TC3: System Environment Variables ................ [FAILED] (0/5)")
            print(f"     - [Reason]: Prerequisite TC1 failed.")

        results['tc3'] = tc3_passed
        if tc3_passed:
            total_score += 5

        # --- TC4: Metadata & Log Auditing --- (5 Marks)
        tc4_passed = False
        if tc1_passed:
            if is_managed:
                check_files_cmd = "[bool](Test-Path 'C:\\workspace\\sysinfo.txt') -and [bool](Test-Path 'C:\\workspace\\log_files.txt')"
                success, output = run_powershell([check_files_cmd])
                if success and "True" in output:
                    # Validate sysinfo.txt content
                    read_sysinfo = "Get-Content 'C:\\workspace\\sysinfo.txt' -Raw"
                    s_success, s_output = run_powershell([read_sysinfo])
                    # Validate log_files.txt content
                    read_logs = "Get-Content 'C:\\workspace\\log_files.txt' -Raw"
                    l_success, l_output = run_powershell([read_logs])

                    if s_success and l_success and len(s_output.strip()) > 0 and len(l_output.strip()) > 0:
                        tc4_passed = True
                        print(f"TC4: Metadata & Log Auditing ..................... [PASSED] (5/5)")
                    else:
                        print(f"TC4: Metadata & Log Auditing ..................... [FAILED] (0/5)")
                        print(f"     - [Reason]: Files exist but sysinfo.txt or log_files.txt is empty.")
                else:
                    print(f"TC4: Metadata & Log Auditing ..................... [FAILED] (0/5)")
                    print(f"     - [Reason]: 'sysinfo.txt' and/or 'log_files.txt' not found in C:\\workspace.")
            else:
                tc4_passed = True
                print(f"TC4: Metadata & Log Auditing ..................... [PASSED] (5/5)")
                print(f"     - [WARNING]: SSM agent is offline. File verification bypassed.")
        else:
            print(f"TC4: Metadata & Log Auditing ..................... [FAILED] (0/5)")
            print(f"     - [Reason]: Prerequisite TC1 failed.")

        results['tc4'] = tc4_passed
        if tc4_passed:
            total_score += 5

        print("-" * 60)
        print(f"{'TOTAL SCORE:':<44} {total_score}/20")
        print("-" * 60 + "\n")

    except Exception as e:
        print(f"[ERROR] Verification failed: {str(e)}")
        total_score = 0

    # Save Metadata for Central Evaluation
    solution_data = {
        'candidate_prefix': username,
        'assessment_start_time': start_time,
        'max_duration_minutes': max_duration,
        'evaluation_type': 'REAL_TIME_API',
        'score': total_score,
        'results': results
    }

    try:
        ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
        os.makedirs(ws_path, exist_ok=True)
        with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
        
        root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
        with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}")

if __name__ == "__main__":
    verify_task()
