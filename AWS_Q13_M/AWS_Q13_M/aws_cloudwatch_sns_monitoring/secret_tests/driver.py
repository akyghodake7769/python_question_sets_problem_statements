import json
import os
import sys
from datetime import datetime, timezone

import boto3

# Capture Assessment Start Time
START_TIME_STR = os.getenv('KODEARENA_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "LOCAL_USER"

def verify_task():
    user_prefix = USER_PREFIX
    start_time = START_TIME_STR
    
    # Standard LabsKraft Header
    print("\n" + "-"*70)
    print(f"{'KODEARENA REAL-TIME AWS AUDIT':^70}")
    print("-"*70)

    total_score = 0
    results = {}

    try:
        # Time Enforcement Logic
        if not START_TIME:
            print("[ERROR] KODEARENA_START_TIME environment variable is missing.")
            raise Exception("Invalid Session")

        now = datetime.now(timezone.utc)
        elapsed_minutes = (now - START_TIME).total_seconds() / 60
        max_duration = 75  # 75 Min assessment

        if elapsed_minutes > max_duration + 5: # 5 min grace
            print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m")
            raise Exception("Time Limit Exceeded")

        print(f"[SYSTEM] Validating Resources for: {user_prefix}")
        print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")

        aws_region = None
        ec2_client = None
        valid_instance = None
        target_instance_id = None
        
        # --- TC1 & TC2: EC2 Instance & IAM Setup ---
        tc1_passed = False
        tc2_passed = False
        
        from datetime import timedelta
        
        for region in ['eu-west-1', 'eu-west-2', 'eu-west-3']:
            temp_ec2 = boto3.client('ec2', region_name=region)
            try:
                instances = temp_ec2.describe_instances(Filters=[
                    {'Name': 'tag:Name', 'Values': [f'labskraft-monitor-ec2-{user_prefix}']},
                    {'Name': 'instance-state-name', 'Values': ['running', 'pending', 'stopped']}
                ])
                
                if instances.get('Reservations'):
                    for res in instances['Reservations']:
                        for inst in res.get('Instances', []):
                            # Allow up to 2 hours of clock skew
                            if START_TIME:
                                if inst.get('LaunchTime') >= (START_TIME - timedelta(hours=2)):
                                    valid_instance = inst
                                    break
                            else:
                                valid_instance = inst
                                break
                        if valid_instance:
                            break
            except Exception:
                pass
                
            if valid_instance:
                aws_region = region
                ec2_client = temp_ec2
                break
                
        if not aws_region:
            aws_region = os.getenv('AWS_DEFAULT_REGION', 'eu-west-1')
            ec2_client = boto3.client('ec2', region_name=aws_region)
            
        sns_client = boto3.client('sns', region_name=aws_region)
        cw_client = boto3.client('cloudwatch', region_name=aws_region)
        
        try:
            
            if valid_instance:
                tc1_passed = True
                target_instance_id = valid_instance.get('InstanceId')
                results['tc1'] = True
                print(f"TC1: EC2 Instance Setup ................................ [PASSED] (4/4)")
                
                if 'IamInstanceProfile' in valid_instance:
                    tc2_passed = True
                    results['tc2'] = True
                    print(f"TC2: IAM Instance Profile Setup ........................ [PASSED] (4/4)")
                else:
                    results['tc2'] = False
                    print(f"TC2: IAM Instance Profile Setup ........................ [FAILED] (0/4)")
                    print(f"     └─ [Reason]: IAM Instance Profile not attached.")
            else:
                results['tc1'] = False
                results['tc2'] = False
                print(f"TC1: EC2 Instance Setup ................................ [FAILED] (0/4)")
                print(f"     └─ [Reason]: EC2 instance missing or created before session start.")
                print(f"TC2: IAM Instance Profile Setup ........................ [FAILED] (0/4)")
                print(f"     └─ [Reason]: Prerequisite failed.")
        except Exception as e:
            results['tc1'] = False
            results['tc2'] = False
            print(f"TC1: EC2 Instance Setup ................................ [FAILED] (0/4)")
            print(f"TC2: IAM Instance Profile Setup ........................ [FAILED] (0/4)")
            print(f"     └─ [Error]: {str(e)}")

        # --- TC3: Amazon SNS Topic Setup ---
        tc3_passed = False
        target_topic_arn = None
        if not results.get('tc1'):
            results['tc3'] = False
            print(f"TC3: Amazon SNS Topic Setup ............................ [FAILED] (0/4)")
            print(f"     └─ [Reason]: Prerequisite failed (TC1 invalid).")
            results['tc4'] = False
            print(f"TC4: CloudWatch Alarm Setup ............................ [FAILED] (0/4)")
            print(f"     └─ [Reason]: Prerequisite failed.")
            results['tc5'] = False
            print(f"TC5: Alarm SNS Configuration ........................... [FAILED] (0/4)")
            print(f"     └─ [Reason]: Prerequisite failed.")
        else:
            try:
                topics = sns_client.list_topics()
                for t in topics.get('Topics', []):
                    if t['TopicArn'].endswith(f':DevOps-Alerts-{user_prefix}'):
                        target_topic_arn = t['TopicArn']
                        break
                
                if target_topic_arn:
                    subs = sns_client.list_subscriptions_by_topic(TopicArn=target_topic_arn)
                    if subs.get('Subscriptions'):
                        tc3_passed = True
                        results['tc3'] = True
                        print(f"TC3: Amazon SNS Topic Setup ............................ [PASSED] (4/4)")
                    else:
                        results['tc3'] = False
                        print(f"TC3: Amazon SNS Topic Setup ............................ [FAILED] (0/4)")
                        print(f"     └─ [Reason]: SNS Topic exists but no email subscription configured.")
                else:
                    results['tc3'] = False
                    print(f"TC3: Amazon SNS Topic Setup ............................ [FAILED] (0/4)")
                    print(f"     └─ [Reason]: SNS Topic DevOps-Alerts-{user_prefix} missing.")
            except Exception as e:
                results['tc3'] = False
                print(f"TC3: Amazon SNS Topic Setup ............................ [FAILED] (0/4)")
                print(f"     └─ [Error]: {str(e)}")
            
            # --- TC4 & TC5: CloudWatch Alarm Configuration ---
            try:
                alarms = cw_client.describe_alarms(AlarmNames=['High-CPU-Alarm'])
                target_alarm = None
                if alarms.get('MetricAlarms'):
                    target_alarm = alarms['MetricAlarms'][0]
                    
                if target_alarm:
                    dimensions = {d['Name']: d['Value'] for d in target_alarm.get('Dimensions', [])}
                    is_correct_instance = dimensions.get('InstanceId') == target_instance_id
                    
                    if target_alarm.get('MetricName') == 'CPUUtilization' and \
                       target_alarm.get('Threshold') == 70.0 and \
                       target_alarm.get('Period') == 300 and \
                       target_alarm.get('EvaluationPeriods') == 1 and \
                       target_alarm.get('Namespace') == 'AWS/EC2' and \
                       is_correct_instance:
                        results['tc4'] = True
                        print(f"TC4: CloudWatch Alarm Setup ............................ [PASSED] (4/4)")
                        
                        if target_topic_arn and target_topic_arn in target_alarm.get('AlarmActions', []):
                            results['tc5'] = True
                            print(f"TC5: Alarm SNS Configuration ........................... [PASSED] (4/4)")
                        else:
                            results['tc5'] = False
                            print(f"TC5: Alarm SNS Configuration ........................... [FAILED] (0/4)")
                            print(f"     └─ [Reason]: Alarm SNS action invalid or not linked to the correct SNS topic.")
                    else:
                        results['tc4'] = False
                        results['tc5'] = False
                        print(f"TC4: CloudWatch Alarm Setup ............................ [FAILED] (0/4)")
                        print(f"     └─ [Reason]: CloudWatch Alarm settings are incorrect (check Threshold, Period, Metric or Target Instance).")
                        print(f"TC5: Alarm SNS Configuration ........................... [FAILED] (0/4)")
                        print(f"     └─ [Reason]: Prerequisite failed.")
                else:
                    results['tc4'] = False
                    results['tc5'] = False
                    print(f"TC4: CloudWatch Alarm Setup ............................ [FAILED] (0/4)")
                    print(f"     └─ [Reason]: CloudWatch Alarm 'High-CPU-Alarm' missing.")
                    print(f"TC5: Alarm SNS Configuration ........................... [FAILED] (0/4)")
                    print(f"     └─ [Reason]: Prerequisite failed.")
            except Exception as e:
                results['tc4'] = False
                results['tc5'] = False
                print(f"TC4: CloudWatch Alarm Setup ............................ [FAILED] (0/4)")
                print(f"TC5: Alarm SNS Configuration ........................... [FAILED] (0/4)")
                print(f"     └─ [Error]: {str(e)}")

        # Final Scoring
        total_score = sum([4 for r in results.values() if r])
        
        print("-" * 70)
        print(f"{'TOTAL SCORE:':<52} {total_score}/20")
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
            
        root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
        with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}")

if __name__ == '__main__':
    verify_task()
