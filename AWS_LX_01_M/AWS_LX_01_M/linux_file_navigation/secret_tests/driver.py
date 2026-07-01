import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
import boto3

START_TIME_STR = os.getenv('KODEBUCK_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', 'LOCAL_USER')

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
    target_instance = f"labskraft-ubuntu-ec2-{username}"
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
    try:
        resp = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [target_instance]}, {'Name': 'instance-state-name', 'Values': ['running']}])
        instances = [i for r in resp.get('Reservations', []) for i in r.get('Instances', [])]
        if instances:
            if instances[0].get('InstanceType') == 't2.micro':
                tc1_passed = True
                instance_id = instances[0]['InstanceId']
    except Exception as e:
        pass

    results['tc1'] = tc1_passed
    if tc1_passed:
        total_score += 5
        print("TC1: EC2 Instance (t2.micro) ............ [PASSED] (5/5)")
    else:
        print("TC1: EC2 Instance (t2.micro) ............ [FAILED] (0/5)")

    def run_ssm(cmd):
        if not instance_id: return None
        try:
            res = ssm.send_command(InstanceIds=[instance_id], DocumentName="AWS-RunShellScript", Parameters={'commands': [cmd]}, TimeoutSeconds=30)
            cmd_id = res['Command']['CommandId']
            for _ in range(15):
                time.sleep(2)
                inv = ssm.get_command_invocation(CommandId=cmd_id, InstanceId=instance_id)
                if inv['Status'] in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
                    return inv.get('StandardOutputContent', '').strip()
        except: pass
        return None

    # TC2
    tc2_passed = False
    if tc1_passed:
        out = run_ssm("test -d /home/ubuntu/app/config && test -d /home/ubuntu/app/logs && echo PASS || echo FAIL")
        if out and "PASS" in out: tc2_passed = True
    results['tc2'] = tc2_passed
    total_score += 5 if tc2_passed else 0
    print(f"TC2: {'Directory hierarchy created':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({5 if tc2_passed else 0}/5)")

    # TC3
    tc3_passed = False
    if tc1_passed:
        out = run_ssm("test -f /home/ubuntu/app/app.conf.backup && test -f /home/ubuntu/search_results.txt && echo PASS || echo FAIL")
        if out and "PASS" in out: tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 5 if tc3_passed else 0
    print(f"TC3: {'File operations completed':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({5 if tc3_passed else 0}/5)")

    # TC4
    tc4_passed = False
    if tc1_passed:
        out = run_ssm("test -s /home/ubuntu/disk_usage.txt && echo PASS || echo FAIL")
        if out and "PASS" in out: tc4_passed = True
    results['tc4'] = tc4_passed
    total_score += 5 if tc4_passed else 0
    print(f"TC4: {'Disk usage output generated':<30} [{'PASSED' if tc4_passed else 'FAILED'}] ({5 if tc4_passed else 0}/5)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/20")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump({'score': total_score, 'results': results}, f, indent=4)

if __name__ == "__main__":
    verify_task()
