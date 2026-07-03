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
    print(f"{'KODEBUCK AWS LINUX VERIFICATION':^60}")
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
        f"labskraft-ubuntu-ec2-{username}"
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

    def run_ssm(cmd):
        if not instance_id: return None
        try:
            res = ssm.send_command(InstanceIds=[instance_id], DocumentName="AWS-RunShellScript", Parameters={'commands': [cmd]}, TimeoutSeconds=60)
            cmd_id = res['Command']['CommandId']
            for _ in range(30):
                time.sleep(2)
                try:
                    inv = ssm.get_command_invocation(CommandId=cmd_id, InstanceId=instance_id)
                    if inv['Status'] in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
                        return inv.get('StandardOutputContent', '').strip()
                except ssm.exceptions.InvocationDoesNotExist:
                    pass
        except Exception as e:
            print(f"[DEBUG] SSM command send failed: {e}")
        return None

    # TC2: User appuser created successfully
    tc2_passed = False
    if tc1_passed:
        out = run_ssm("id appuser >/dev/null 2>&1 && echo PASS || echo FAIL")
        if out and "PASS" in out: tc2_passed = True
    results['tc2'] = tc2_passed
    total_score += 4 if tc2_passed else 0
    print(f"TC2: {'User appuser created':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({4 if tc2_passed else 0}/4)")

    # TC3: Directory secure_data and files created
    tc3_passed = False
    if tc1_passed:
        out = run_ssm("test -d /home/ubuntu/secure_data && test -f /home/ubuntu/secure_data/passwords.txt && test -f /home/ubuntu/secure_data/config.ini && echo PASS || echo FAIL")
        if out and "PASS" in out: tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 4 if tc3_passed else 0
    print(f"TC3: {'Files and directory created':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({4 if tc3_passed else 0}/4)")

    # TC4: Permissions applied
    tc4_passed = False
    if tc1_passed:
        out1 = run_ssm("stat -c '%a' /home/ubuntu/secure_data/passwords.txt")
        out2 = run_ssm("stat -c '%a' /home/ubuntu/secure_data/config.ini")
        if out1 and "400" in out1 and out2 and "755" in out2:
            tc4_passed = True
    results['tc4'] = tc4_passed
    total_score += 4 if tc4_passed else 0
    print(f"TC4: {'Proper permissions applied':<30} [{'PASSED' if tc4_passed else 'FAILED'}] ({4 if tc4_passed else 0}/4)")

    # TC5: Ownership configured correctly
    tc5_passed = False
    if tc1_passed:
        out = run_ssm("stat -c '%U' /home/ubuntu/secure_data/config.ini")
        if out and "appuser" in out: tc5_passed = True
    results['tc5'] = tc5_passed
    total_score += 4 if tc5_passed else 0
    print(f"TC5: {'Ownership configured correctly':<30} [{'PASSED' if tc5_passed else 'FAILED'}] ({4 if tc5_passed else 0}/4)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/20")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump({'score': total_score, 'results': results}, f, indent=4)

if __name__ == "__main__":
    verify_task()
