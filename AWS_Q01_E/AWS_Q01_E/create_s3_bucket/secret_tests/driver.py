# import boto3
# import os
# import sys
# import json
# from datetime import datetime, timezone, timedelta

# # 1. Setup AWS Client (Credentials picked up from environment variables)
# def get_s3_client():
#     try:
#         return boto3.client('s3')
#     except Exception as e:
#         print(f"FAILED: Could not connect to AWS. Error: {e}")
#         sys.exit(1)

# def get_iam_username():
#     try:
#         import boto3
#         sts = boto3.client('sts')
#         arn = sts.get_caller_identity().get('Arn', '')
#         if ':user/' in arn:
#             return arn.split(':user/')[-1].strip()
#         elif ':assumed-role/' in arn:
#             role_part = arn.split(':assumed-role/')[-1].strip()
#             if '/' in role_part:
#                 return role_part.split('/')[-1].strip()
#             return role_part.strip()
#         else:
#             if '/' in arn:
#                 return arn.split('/')[-1].strip()
#     except Exception:
#         pass
#     return None

# def resolve_username(default_prefix):
#     if default_prefix and default_prefix != 'LOCAL_USER':
#         return default_prefix
#     iam_user = get_iam_username()
#     if iam_user and iam_user not in ['root', 'ubuntu', 'administrator', 'SYSTEM', 'LOCAL_USER']:
#         return iam_user
#     return default_prefix

# def verify_task(username=None, exam_code_arg=None):
#     s3 = get_s3_client()

#     if username is None:
#         username = os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER')
    
#     username = resolve_username(username)
    
#     if exam_code_arg is None:
#         exam_code_arg = sys.argv[3] if len(sys.argv) > 3 else (os.getenv('KODEBUCK_EXAM_CODE') or os.getenv('EXAM_CODE') or 'UNKNOWN')

#     target_bucket = f"{username}-{exam_code_arg}"

#     print("-" * 40)
#     print("AWS RESOURCE VERIFICATION REPORT")
#     print(f"Target Bucket: {target_bucket}")
#     print("-" * 40)

#     total_score = 0
#     results = {}

#     # --- TEST CASE 1: BUCKET EXISTENCE ---
#     try:
#         s3.head_bucket(Bucket=target_bucket)
#         print("TC1 [Bucket Creation] (5/5) - Success: Bucket found in AWS.")
#         results['tc1'] = True
#         total_score += 5
#     except Exception:
#         print("TC1 [Bucket Creation] (0/5) - Failed: Bucket not found.")
#         results['tc1'] = False

#     if not results.get('tc1'):
#         results['tc2'] = False
#         results['tc3'] = False
#         print("TC2 [Public Access Blocked] (0/5) - Skipped: Bucket not found.")
#         print("TC3 [Region Check] (0/5) - Skipped: Bucket not found.")
#         print("-" * 40)
#         print(f"TOTAL SCORE: {total_score}/15")
#         print("-" * 40)
#         return total_score, results

#     # --- TEST CASE 2: PUBLIC ACCESS BLOCK ---
#     try:
#         pab = s3.get_public_access_block(Bucket=target_bucket)
#         config = pab.get('PublicAccessBlockConfiguration', {})
#         if config.get('BlockPublicAcls') and config.get('BlockPublicPolicy'):
#             print("TC2 [Public Access Blocked] (5/5) - Success: Security configured.")
#             results['tc2'] = True
#             total_score += 5
#         else:
#             print("TC2 [Public Access Blocked] (0/5) - Failed: Public access is still allowed.")
#             results['tc2'] = False
#     except Exception:
#         print("TC2 [Public Access Blocked] (0/5) - Failed: Security settings not found.")
#         results['tc2'] = False

#     # --- TEST CASE 3: REGION CHECK ---
#     try:
#         location = s3.get_bucket_location(Bucket=target_bucket)
#         region = location.get('LocationConstraint') or 'us-east-1'
#         if region in ['eu-west-1', 'eu-west-2', 'eu-west-3']:
#             print(f"TC3 [Region Check] (5/5) - Success: Correct region '{region}' used.")
#             results['tc3'] = True
#             total_score += 5
#         else:
#             print(f"TC3 [Region Check] (0/5) - Failed: Found in {region}.")
#             results['tc3'] = False
#     except Exception:
#         print("TC3 [Region Check] (0/5) - Failed: Error retrieving location.")
#         results['tc3'] = False

#     print("-" * 40)
#     print(f"TOTAL SCORE: {total_score}/15")
#     print("-" * 40)

#     return total_score, results
# if __name__ == "__main__":
#     verify_task()
import boto3
import os
import sys
import json
from datetime import datetime, timezone, timedelta

# 1. Setup AWS Client (Credentials picked up from environment variables)
def get_s3_client():
    try:
        return boto3.client('s3')
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

def verify_task(username=None, exam_code_arg=None):
    s3 = get_s3_client()

    if username is None:
        username = os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER')
    
    username = resolve_username(username)
    
    if exam_code_arg is None:
        exam_code_arg = sys.argv[3] if len(sys.argv) > 3 else (os.getenv('KODEBUCK_EXAM_CODE') or os.getenv('EXAM_CODE') or 'UNKNOWN')

    target_bucket = f"{username}-{exam_code_arg}"

    print("-" * 40)
    print("AWS RESOURCE VERIFICATION REPORT")
    print(f"Target Bucket: {target_bucket}")
    print("-" * 40)

    total_score = 0
    results = {}

    # --- TEST CASE 1: BUCKET EXISTENCE ---
    try:
        s3.head_bucket(Bucket=target_bucket)
        print("TC1 [Bucket Creation] (5/5) - Success: Bucket found in AWS.")
        results['tc1'] = True
        total_score += 5
    except Exception:
        print("TC1 [Bucket Creation] (0/5) - Failed: Bucket not found.")
        results['tc1'] = False

    if not results.get('tc1'):
        results['tc2'] = False
        results['tc3'] = False
        print("TC2 [Public Access Blocked] (0/5) - Skipped: Bucket not found.")
        print("TC3 [Region Check] (0/5) - Skipped: Bucket not found.")
        print("-" * 40)
        print(f"TOTAL SCORE: {total_score}/15")
        print("-" * 40)
        return total_score, results

    # --- TEST CASE 2: PUBLIC ACCESS BLOCK ---
    try:
        pab = s3.get_public_access_block(Bucket=target_bucket)
        config = pab.get('PublicAccessBlockConfiguration', {})
        if config.get('BlockPublicAcls') and config.get('BlockPublicPolicy'):
            print("TC2 [Public Access Blocked] (5/5) - Success: Security configured.")
            results['tc2'] = True
            total_score += 5
        else:
            print("TC2 [Public Access Blocked] (0/5) - Failed: Public access is still allowed.")
            results['tc2'] = False
    except Exception:
        print("TC2 [Public Access Blocked] (0/5) - Failed: Security settings not found.")
        results['tc2'] = False

    # --- TEST CASE 3: REGION CHECK ---
    try:
        location = s3.get_bucket_location(Bucket=target_bucket)
        region = location.get('LocationConstraint') or 'us-east-1'
        if region in ['eu-west-1', 'eu-west-2', 'eu-west-3']:
            print(f"TC3 [Region Check] (5/5) - Success: Correct region '{region}' used.")
            results['tc3'] = True
            total_score += 5
        else:
            print(f"TC3 [Region Check] (0/5) - Failed: Found in {region}.")
            results['tc3'] = False
    except Exception:
        print("TC3 [Region Check] (0/5) - Failed: Error retrieving location.")
        results['tc3'] = False

    # Save Metadata for Central Evaluation
    start_time_str = os.getenv('KODEBUCK_START_TIME')
    start_time = start_time_str if start_time_str else datetime.now(timezone.utc).isoformat()
    
    solution_data = {
        'candidate_prefix': username,
        'assessment_start_time': start_time,
        'max_duration_minutes': 30,
        'evaluation_type': 'REAL_TIME_API',
        'score': total_score,
        'results': results,
        'exam_code': exam_code_arg
    }

    try:
        ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
        os.makedirs(ws_path, exist_ok=True)
        with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}")

    return total_score, results
if __name__ == "__main__":
    verify_task()
