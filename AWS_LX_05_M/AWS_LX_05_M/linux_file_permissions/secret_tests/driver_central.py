import json
import os
import sys
from datetime import datetime, timezone, timedelta

# Global IST offset for consistent reporting
ist_offset = timezone(timedelta(hours=5, minutes=30))

def verify_task_central(username, start_time_str, exam_code="UNKNOWN"):
    print(f"\n--- Central Validation for {username} ---")
    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'solution.json'))
    try:
        with open(ws_path, 'r') as f:
            data = json.load(f)
            score = data.get('score', 0)
            results = data.get('results', {})
            print(f"Score retrieved: {score}/20")
    except Exception as e:
        print("Failed to read local verification results.")
        score = 0
        results = {}

    report_items = []
    tc_names = {
        'tc1': 'TC1 [User appuser]',
        'tc2': 'TC2 [File Operations]',
        'tc3': 'TC3 [Permissions]',
        'tc4': 'TC4 [Ownership]'
    }
    
    fail_count = 0
    for tc, name in tc_names.items():
        passed = results.get(tc, False)
        marks = 5 if passed else 0
        if not passed:
            fail_count += 1
        report_items.append(f"{name} ({marks}/5)")

    date_str = datetime.now(ist_offset).strftime("%d-%m-%Y")
    timestamp_str = datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")
    problem_code = "AWS_LX_05_M"
    
    csv_report = f"{date_str},{problem_code},{username},{timestamp_str},{len(report_items)}: {'; '.join(report_items)},{exam_code},{fail_count},{score}"
    print(f"\n[REPORT_CSV]: {csv_report}")
    return score, results
