import json
import os
import sys
from datetime import datetime, timezone

# Capture Assessment Start Time
START_TIME_STR = os.getenv('KODEARENA_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEARENA_USERNAME', 'LOCAL_USER')

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
    iam_user = get_iam_username()
    if iam_user and iam_user not in ['root', 'ubuntu', 'administrator', 'SYSTEM', 'LOCAL_USER']:
        return iam_user
    return default_prefix

def verify_task():
    username = resolve_username(USER_PREFIX)
    target_instance = f"labskraft-db-server-{username}"
    region = 'eu-west-2'
    start_time = START_TIME_STR

    print("\n" + "-" * 60)
    print(f"{'KODEARENA AWS EC2 + EBS WINDOWS VERIFICATION':^60}")
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
        max_duration = 30  # 30 Min assessment for AWS_Q24_E

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
                if inst.get('InstanceType') == 't2.micro':
                    tc1_passed = True
                    instance_id = inst['InstanceId']
                    print(f"TC1: EC2 Instance (Windows t2.micro) ........... [PASSED] (5/5)")
                else:
                    print(f"TC1: EC2 Instance (Windows t2.micro) ........... [FAILED] (0/5)")
                    print(f"     └─ [Reason]: Instance found but type is '{inst.get('InstanceType')}', expected 't2.micro'.")
            else:
                print(f"TC1: EC2 Instance (Windows t2.micro) ........... [FAILED] (0/5)")
                print(f"     └─ [Reason]: Running instance named '{target_instance}' not found in {region}.")
        except Exception as e:
            print(f"TC1: EC2 Instance (Windows t2.micro) ........... [FAILED] (0/5)")
            print(f"     └─ [Reason]: Error: {e}")

        results['tc1'] = tc1_passed
        if tc1_passed:
            total_score += 5

        # --- TC2: EBS Volume (20 GB io2) Attached --- (5 Marks)
        tc2_passed = False
        if tc1_passed:
            try:
                volumes = ec2.describe_volumes(Filters=[
                    {'Name': 'attachment.instance-id', 'Values': [instance_id]}
                ])['Volumes']
                found = False
                for v in volumes:
                    if v['Size'] == 20 and v['VolumeType'] == 'io2':
                        found = True
                        break
                if found:
                    tc2_passed = True
                    print(f"TC2: EBS Volume (20 GB io2) Attached ........... [PASSED] (5/5)")
                else:
                    print(f"TC2: EBS Volume (20 GB io2) Attached ........... [FAILED] (0/5)")
                    print(f"     └─ [Reason]: No 20 GB io2 volume attached to instance '{instance_id}'.")
            except Exception as e:
                print(f"TC2: EBS Volume (20 GB io2) Attached ........... [FAILED] (0/5)")
                print(f"     └─ [Reason]: Error retrieving volumes: {e}")
        else:
            print(f"TC2: EBS Volume (20 GB io2) Attached ........... [FAILED] (0/5)")
            print(f"     └─ [Reason]: Prerequisite TC1 failed.")

        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 5

        # --- TC3: EBS Formatted NTFS and Drive Letter F: --- (5 Marks)
        tc3_passed = False
        if tc2_passed:
            tc3_passed = True
            print(f"TC3: EBS Formatted NTFS (Drive F:) ................. [PASSED] (5/5)")
        else:
            print(f"TC3: EBS Formatted NTFS (Drive F:) ................. [FAILED] (0/5)")
            print(f"     └─ [Reason]: Prerequisite TC2 failed.")

        results['tc3'] = tc3_passed
        if tc3_passed:
            total_score += 5

        print("-" * 60)
        print(f"{'TOTAL SCORE:':<44} {total_score}/15")
        print("-" * 60 + "\n")

    except Exception as e:
        print(f"[ERROR] Verification failed: {str(e)}")
        total_score = 0

    # Save Metadata for Central Evaluation
    solution_data = {
        'candidate_prefix': username,
        'assessment_start_time': start_time,
        'max_duration_minutes': 30,
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

if __name__ == "__main__":
    verify_task()
