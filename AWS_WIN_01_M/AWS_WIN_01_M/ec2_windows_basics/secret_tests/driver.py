import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
import urllib.request
import csv
import boto3

START_TIME_STR = os.getenv('KODEBUCK_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', 'LOCAL_USER')

def get_exam_codes_from_sheet(username):
    codes = []
    env_code = os.getenv('KODEBUCK_EXAM_CODE')
    if env_code:
        codes.append(env_code.strip())
    
    try:
        url = "https://docs.google.com/spreadsheets/d/14MJnX-lIvWYKWQ7lZ2boKNYYmCauW40LJ5guEf3BRm8/export?format=csv&gid=0"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            lines = [line.decode('utf-8') for line in response.readlines()]
            reader = csv.reader(lines)
            next(reader) # skip header
            for row in reader:
                if len(row) >= 3 and row[2].strip() == username:
                    code = row[1].strip()
                    if code and code not in codes:
                        codes.append(code)
    except Exception as e:
        pass
    
    if not codes:
        codes.append("UNKNOWN")
    return codes

def get_iam_username():
    try:
        sts = boto3.client('sts')
        arn = sts.get_caller_identity().get('Arn', '')
        if ':user/' in arn: return arn.split(':user/')[-1].strip()
        elif ':assumed-role/' in arn: return arn.split(':assumed-role/')[-1].split('/')[-1].strip()
        return arn.split('/')[-1].strip()
    except: return None

def verify_task():
    username = USER_PREFIX if USER_PREFIX != 'LOCAL_USER' else (get_iam_username() or USER_PREFIX)
    region = 'eu-west-2'
    start_time = START_TIME_STR or datetime.now(timezone.utc).isoformat()

    print("\n" + "-" * 60)
    print(f"{'KODEBUCK AWS WINDOWS BASICS VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}
    
    ec2 = boto3.client('ec2', region_name=region)
    ssm = boto3.client('ssm', region_name=region)

    tc1_passed = False
    instance_id = None
    
    exam_codes = get_exam_codes_from_sheet(username)
    possible_names = []
    for ec in exam_codes:
        possible_names.append(f"{username}-{ec}")
    possible_names.extend([
        username,
        f"labskraft-windows-basics-{username}"
    ])

    try:
        resp = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        instances = [i for r in resp.get('Reservations', []) for i in r.get('Instances', [])]
        for inst in instances:
            name = next((t['Value'] for t in inst.get('Tags', []) if t['Key'] == 'Name'), None)
            if name in possible_names:
                if inst.get('InstanceType') == 't2.micro':
                    tc1_passed = True
                    instance_id = inst['InstanceId']
                    break
    except Exception as e:
        pass

    results['tc1'] = tc1_passed
    if tc1_passed:
        total_score += 4
        print("TC1: EC2 Instance (t2.micro) ............ [PASSED] (4/4)")
    else:
        print("TC1: EC2 Instance (t2.micro) ............ [FAILED] (0/4)")

    is_managed = False
    if tc1_passed:
        try:
            ssm_instances = ssm.describe_instance_information(
                Filters=[{'Key': 'InstanceIds', 'Values': [instance_id]}]
            ).get('InstanceInformationList', [])
            if ssm_instances and ssm_instances[0].get('PingStatus') == 'Online':
                is_managed = True
        except Exception:
            pass

    def run_powershell(commands):
        if not instance_id: return None
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

    # TC2: Directory Structure
    tc2_passed = False
    if tc1_passed:
        if is_managed:
            cmd = "[bool](Test-Path 'C:\\workspace\\logs') -and [bool](Test-Path 'C:\\workspace\\backups')"
            success, output = run_powershell([cmd])
            if success and "True" in output:
                tc2_passed = True
        if tc2_passed:
            print(f"TC2: {'Directory Structure created':<30} [PASSED] (4/4)")
        else:
            print(f"TC2: {'Directory Structure created':<30} [FAILED] (0/4)")
            if not is_managed:
                print("     - [Reason]: SSM agent is offline on the instance. Cannot perform verification.")
    else:
        print(f"TC2: {'Directory Structure created':<30} [FAILED] (0/4)")
        print("     - [Reason]: Prerequisite TC1 failed.")
    results['tc2'] = tc2_passed
    total_score += 4 if tc2_passed else 0

    # TC3: System Environment Variables
    tc3_passed = False
    if tc1_passed:
        if is_managed:
            cmd = "[Environment]::GetEnvironmentVariable('APP_ENVIRONMENT', 'Machine')"
            success, output = run_powershell([cmd])
            if success and output == "production":
                tc3_passed = True
        if tc3_passed:
            print(f"TC3: {'System Env Variables set':<30} [PASSED] (4/4)")
        else:
            print(f"TC3: {'System Env Variables set':<30} [FAILED] (0/4)")
            if not is_managed:
                print("     - [Reason]: SSM agent is offline. Cannot perform verification.")
    else:
        print(f"TC3: {'System Env Variables set':<30} [FAILED] (0/4)")
        print("     - [Reason]: Prerequisite TC1 failed.")
    results['tc3'] = tc3_passed
    total_score += 4 if tc3_passed else 0

    # TC4: Metadata Auditing (sysinfo.txt)
    tc4_passed = False
    if tc1_passed:
        if is_managed:
            cmd = "[bool](Test-Path 'C:\\workspace\\sysinfo.txt')"
            success, output = run_powershell([cmd])
            if success and "True" in output:
                read_cmd = "Get-Content 'C:\\workspace\\sysinfo.txt' -Raw"
                r_success, r_output = run_powershell([read_cmd])
                if r_success and len(r_output.strip()) > 0:
                    tc4_passed = True
        if tc4_passed:
            print(f"TC4: {'Metadata Auditing (sysinfo)':<30} [PASSED] (4/4)")
        else:
            print(f"TC4: {'Metadata Auditing (sysinfo)':<30} [FAILED] (0/4)")
            if not is_managed:
                print("     - [Reason]: SSM agent is offline. Cannot perform verification.")
    else:
        print(f"TC4: {'Metadata Auditing (sysinfo)':<30} [FAILED] (0/4)")
        print("     - [Reason]: Prerequisite TC1 failed.")
    results['tc4'] = tc4_passed
    total_score += 4 if tc4_passed else 0

    # TC5: Log Auditing (log_files.txt)
    tc5_passed = False
    if tc1_passed:
        if is_managed:
            cmd = "[bool](Test-Path 'C:\\workspace\\log_files.txt')"
            success, output = run_powershell([cmd])
            if success and "True" in output:
                read_cmd = "Get-Content 'C:\\workspace\\log_files.txt' -Raw"
                r_success, r_output = run_powershell([read_cmd])
                if r_success and len(r_output.strip()) > 0:
                    tc5_passed = True
        if tc5_passed:
            print(f"TC5: {'Log Auditing (log_files)':<30} [PASSED] (4/4)")
        else:
            print(f"TC5: {'Log Auditing (log_files)':<30} [FAILED] (0/4)")
            if not is_managed:
                print("     - [Reason]: SSM agent is offline. Cannot perform verification.")
    else:
        print(f"TC5: {'Log Auditing (log_files)':<30} [FAILED] (0/4)")
        print("     - [Reason]: Prerequisite TC1 failed.")
    results['tc5'] = tc5_passed
    total_score += 4 if tc5_passed else 0

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/20")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump({'score': total_score, 'results': results}, f, indent=4)
