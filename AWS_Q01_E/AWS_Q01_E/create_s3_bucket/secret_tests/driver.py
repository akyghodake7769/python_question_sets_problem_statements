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

def verify_task(username=None, exam_code_arg=None):
    s3 = get_s3_client()

    if username is None:
        username = os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER')
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

    print("-" * 40)
    print(f"TOTAL SCORE: {total_score}/15")
    print("-" * 40)

    return total_score, results


def verify_aws_on_server(candidate_email, question_id, labskraft_username=None, assessment_start_time=None, solution_data=None, exam_code_arg="UNKNOWN"):
    """
    Central Server Auditor: Verifies AWS S3 bucket setup.
    This fallback version uses environment-variable credentials.
    """
    # Resolve username
    if solution_data and 'candidate_prefix' in solution_data:
        username = solution_data['candidate_prefix']
    else:
        username = labskraft_username if labskraft_username else candidate_email.split('@')[0]

    # Resolve exam_code
    exam_code = exam_code_arg
    if (not exam_code or exam_code == 'UNKNOWN') and solution_data:
        exam_code = solution_data.get('exam_code') or solution_data.get('question_id') or 'UNKNOWN'

    # Run the verification
    total_score, results = verify_task(username=username, exam_code_arg=exam_code)

    # Build report
    ist_offset = timezone(timedelta(hours=5, minutes=30))
    date_str = datetime.now(ist_offset).strftime("%d-%m-%Y")
    time_str = datetime.now(ist_offset).strftime("%H:%M:%S")
    timestamp = datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")

    problem_code = "create_s3_bucket"
    tc_names = {
        'tc1': 'TC1 [Bucket Creation]',
        'tc2': 'TC2 [Public Access Blocked]',
        'tc3': 'TC3 [Region Check]'
    }
    passed_cases = [tc_names[tc] for tc in ['tc1', 'tc2', 'tc3'] if results.get(tc)]
    failed_cases  = [tc_names[tc] for tc in ['tc1', 'tc2', 'tc3'] if not results.get(tc)]

    passed_str = f"{len(passed_cases)}: {'; '.join(passed_cases)}" if passed_cases else "0"
    failed_str  = f"{len(failed_cases)}: {'; '.join(failed_cases)}"  if failed_cases  else "0"

    csv_report = f"{date_str},{problem_code},{exam_code.upper()},{username},{time_str},{passed_str},{failed_str},{total_score}"

    # Save report to central server filesystem
    report_base = f"/home/ubuntu/central_server/reports/{problem_code}/{candidate_email}"
    try:
        os.makedirs(report_base, exist_ok=True)
        report_path = os.path.join(report_base, f"{candidate_email}_{timestamp}.txt")
        file_results = [
            "-" * 60,
            f"{'KODEBUCK AWS S3 BUCKET VERIFICATION':^60}",
            "-" * 60,
            f"{'✓' if results.get('tc1') else '✗'} TC1: Bucket Creation ............... {'PASSED (5/5)' if results.get('tc1') else 'FAILED (0/5)'}",
            f"{'✓' if results.get('tc2') else '✗'} TC2: Public Access Blocked ......... {'PASSED (5/5)' if results.get('tc2') else 'FAILED (0/5)'}",
            f"{'✓' if results.get('tc3') else '✗'} TC3: Region Check .................. {'PASSED (5/5)' if results.get('tc3') else 'FAILED (0/5)'}",
            "-" * 60,
            f"TOTAL SCORE: {total_score}/15",
            "-" * 60,
        ]
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(file_results) + "\n")
    except Exception as e:
        print(f"[WARN] Could not write report file: {e}")

    print(f"\n[REPORT_CSV]{csv_report}")
    return total_score, results


if __name__ == "__main__":
    verify_task()
