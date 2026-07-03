import sys
import json
import os
from datetime import datetime, timezone, timedelta

def verify_aws_on_server(candidate_email, question_id, labskraft_username=None, assessment_start_time=None, solution_data=None, exam_code="UNKNOWN"):
    """
    Central Server Auditor: Verifies AWS Windows Server Basics setup.
    """
    if solution_data and 'candidate_prefix' in solution_data:
        username = solution_data['candidate_prefix']
    else:
        username = labskraft_username if labskraft_username else candidate_email.split('@')[0]
    
    report_items = []
    file_results = []
    fail_count = 0
    total_score = 0
    
    results = solution_data.get('results', {}) if solution_data else {}
    
    # --- TC1: EC2 Instance Provisioning ---
    tc1_passed = results.get('tc1', False)
    if tc1_passed:
        report_items.append("TC1 [EC2 Instance Provisioning] (5/5)")
        file_results.append("✓ TC1 [EC2 Instance Provisioning]: PASSED (5/5)")
        total_score += 5
    else:
        report_items.append("TC1 [EC2 Instance Provisioning] (0/5)")
        file_results.append(f"✗ TC1 [EC2 Instance Provisioning]: FAILED (0/5) | Running Windows EC2 instance named labskraft-windows-basics-{username} not found.")
        fail_count += 1

    # --- TC2: Directory Structure ---
    tc2_passed = results.get('tc2', False)
    if tc2_passed:
        report_items.append("TC2 [Directory Structure] (5/5)")
        file_results.append("✓ TC2 [Directory Structure]: PASSED (5/5)")
        total_score += 5
    else:
        report_items.append("TC2 [Directory Structure] (0/5)")
        file_results.append("✗ TC2 [Directory Structure]: FAILED (0/5) | Directories 'C:\\workspace\\logs' and/or 'C:\\workspace\\backups' do not exist.")
        fail_count += 1

    # --- TC3: System Environment Variables ---
    tc3_passed = results.get('tc3', False)
    if tc3_passed:
        report_items.append("TC3 [System Environment Variables] (5/5)")
        file_results.append("✓ TC3 [System Environment Variables]: PASSED (5/5)")
        total_score += 5
    else:
        report_items.append("TC3 [System Environment Variables] (0/5)")
        file_results.append("✗ TC3 [System Environment Variables]: FAILED (0/5) | System-level environment variable 'APP_ENVIRONMENT' not set to 'production'.")
        fail_count += 1

    # --- TC4: Metadata & Log Auditing ---
    tc4_passed = results.get('tc4', False)
    if tc4_passed:
        report_items.append("TC4 [Metadata & Log Auditing] (5/5)")
        file_results.append("✓ TC4 [Metadata & Log Auditing]: PASSED (5/5)")
        total_score += 5
    else:
        report_items.append("TC4 [Metadata & Log Auditing] (0/5)")
        file_results.append("✗ TC4 [Metadata & Log Auditing]: FAILED (0/5) | Files 'sysinfo.txt' and/or 'log_files.txt' not found or empty in C:\\workspace.")
        fail_count += 1

    file_results.append("-" * 50)
    file_results.append(f"🎯 TOTAL SCORE: {total_score}/20")

    # 8-Column CSV Format for Taxila LMS
    ist_offset = timezone(timedelta(hours=5, minutes=30))
    date_str = datetime.now(ist_offset).strftime("%d-%m-%Y")
    timestamp = datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")
    
    problem_code = "AWS_WIN_01_M"
    csv_report = f"{date_str},{problem_code},{candidate_email},{timestamp},{len(report_items)}: {'; '.join(report_items)},{exam_code},{fail_count},{total_score}"
    
    # Save Report to Central Server Filesystem
    report_base = f"/home/ubuntu/central_server/reports/{problem_code}/{candidate_email}"
    os.makedirs(report_base, exist_ok=True)
    report_path = os.path.join(report_base, f"{candidate_email}_{timestamp}.txt")
    
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(file_results) + "\n")
    except Exception as e:
        print(f"[WARN] Could not write report file: {e}")
        pass
    
    print(f"\n[REPORT_CSV]: {csv_report}")
    return csv_report

if __name__ == "__main__":
    if len(sys.argv) > 1:
        verify_aws_on_server(sys.argv[1], "AWS_WIN_01_M")
    else:
        verify_aws_on_server("candidate@labskraft.com", "AWS_WIN_01_M")
