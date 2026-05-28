import boto3, os, sys, json
from datetime import datetime, timezone

START_TIME_STR = os.getenv('KLOUDKRAFT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "LOCAL_USER"

def verify_task():
    print("\n" + "-"*70)
    print(f"{'KODEARENA REAL-TIME AWS AUDIT':^70}")
    print("-" * 70)

    username = os.getenv('KLOUDKRAFT_USERNAME', USER_PREFIX)
    bucket_name = f"terraform-state-bucket-{username}"
    table_name = f"terraform-lock-table-{username}"
    
    results = {}
    total_score = 0
    
    try: s3 = boto3.client('s3')
    except Exception as e: print(f"[ERROR] AWS Connection Failed: {e}"); return
    try: dynamodb = boto3.client('dynamodb')
    except: pass
    
    # TC1: S3 Bucket Existence
    tc1_passed = False
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"TC1: S3 Bucket Existence ..................................... [PASSED] (4/4)")
        results['tc1'] = True; total_score += 4
        tc1_passed = True
    except:
        print(f"TC1: S3 Bucket Existence ..................................... [FAILED] (0/4)")
        print(f"     └─ [Reason]: S3 bucket '{bucket_name}' does not exist or access denied.")
        results['tc1'] = False

    # TC2: Versioning
    if tc1_passed:
        try:
            ver = s3.get_bucket_versioning(Bucket=bucket_name)
            if ver.get('Status') == 'Enabled':
                print(f"TC2: S3 Bucket Versioning Enabled ................................ [PASSED] (3/3)")
                results['tc2'] = True; total_score += 3
            else:
                print(f"TC2: S3 Bucket Versioning Enabled ................................ [FAILED] (0/3)")
                print(f"     └─ [Reason]: S3 bucket versioning status is not 'Enabled'.")
                results['tc2'] = False
        except Exception as e:
            print(f"TC2: S3 Bucket Versioning Enabled ................................ [FAILED] (0/3)")
            print(f"     └─ [Reason]: Failed to check versioning: {str(e)}")
            results['tc2'] = False
            
        # TC3: Encryption
        try:
            enc = s3.get_bucket_encryption(Bucket=bucket_name)
            rules = enc.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
            if rules and rules[0].get('ApplyServerSideEncryptionByDefault'):
                print(f"TC3: S3 Bucket Encryption Enabled ................................ [PASSED] (3/3)")
                results['tc3'] = True; total_score += 3
            else:
                print(f"TC3: S3 Bucket Encryption Enabled ................................ [FAILED] (0/3)")
                print(f"     └─ [Reason]: Default server-side encryption is not configured.")
                results['tc3'] = False
        except Exception as e:
            print(f"TC3: S3 Bucket Encryption Enabled ................................ [FAILED] (0/3)")
            print(f"     └─ [Reason]: Default encryption is disabled or failed to check: {str(e)}")
            results['tc3'] = False
    else:
        print(f"TC2: S3 Bucket Versioning Enabled ................................ [FAILED] (0/3)")
        print(f"     └─ [Reason]: Prerequisite failed (S3 bucket does not exist).")
        results['tc2'] = False
        print(f"TC3: S3 Bucket Encryption Enabled ................................ [FAILED] (0/3)")
        print(f"     └─ [Reason]: Prerequisite failed (S3 bucket does not exist).")
        results['tc3'] = False

    # TC4: DynamoDB Table Existence
    tc4_passed = False
    try:
        desc = dynamodb.describe_table(TableName=table_name)['Table']
        print(f"TC4: DynamoDB Table Existence ............................. [PASSED] (4/4)")
        results['tc4'] = True; total_score += 4
        tc4_passed = True
        
        # TC5: Partition Key is LockID
        keys = desc.get('KeySchema', [])
        if keys and keys[0].get('AttributeName') == 'LockID':
            print(f"TC5: DynamoDB Partition Key is LockID ........................... [PASSED] (3/3)")
            results['tc5'] = True; total_score += 3
        else:
            print(f"TC5: DynamoDB Partition Key is LockID ........................... [FAILED] (0/3)")
            print(f"     └─ [Reason]: Table partition key (Hash Key) is not 'LockID'.")
            results['tc5'] = False
    except:
        print(f"TC4: DynamoDB Table Existence ............................. [FAILED] (0/4)")
        print(f"     └─ [Reason]: DynamoDB table '{table_name}' was not found.")
        results['tc4'] = False
        print(f"TC5: DynamoDB Partition Key is LockID ........................... [FAILED] (0/3)")
        print(f"     └─ [Reason]: Prerequisite failed (DynamoDB table does not exist).")
        results['tc5'] = False

    # TC6: Terraform Execution check
    tf_executed = False
    ws_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    if os.path.exists(os.path.join(ws_dir, '.terraform')) or os.path.exists(os.path.join(ws_dir, '.terraform.lock.hcl')) or os.path.exists(os.path.join(ws_dir, 'terraform.tfstate')):
        tf_executed = True

    if not tf_executed:
        history_paths = [
            os.path.expanduser('~/.bash_history'),
            '/home/ubuntu/.bash_history',
            '.bash_history'
        ]
        for path in history_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        history = f.read()
                        if 'terraform init' in history or 'terraform apply' in history or 'terraform plan' in history:
                            tf_executed = True
                            break
                except:
                    pass

    if not tf_executed:
        log_paths = [
            '/home/ubuntu/terraform.log',
            '/tmp/terraform.log',
            'terraform.log'
        ]
        for path in log_paths:
            if os.path.exists(path):
                tf_executed = True
                break

    if tf_executed:
        print(f"TC6: Terraform Execution Status Checked .................... [PASSED] (3/3)")
        results['tc6'] = True; total_score += 3
    else:
        print(f"TC6: Terraform Execution Status Checked .................... [FAILED] (0/3)")
        print(f"     └─ [Reason]: Terraform was not executed/initialized on Ubuntu VM (missing state, SCM cache or CLI history).")
        results['tc6'] = False
        
    print("-" * 70)
    print(f"{'TOTAL SCORE:':<52} {total_score}/20")
    print("-" * 70 + "\n")
    
    solution_data = {
        'candidate_prefix': username,
        'assessment_start_time': START_TIME_STR,
        'evaluation_type': 'REAL_TIME_API',
        'score': total_score,
        'results': results
    }
    
    try:
        ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
        os.makedirs(ws_path, exist_ok=True)
        with open(os.path.join(ws_path, 'solution.json'), 'w') as f: json.dump(solution_data, f, indent=4)
    except: pass

if __name__ == "__main__":
    verify_task()
