import os
import sys
import subprocess
import re
from datetime import datetime, timezone, timedelta

def get_ist_time():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y%m%d_%H%M%S")

def run_test(input_str, harness_dir):
    try:
        parent_dir = os.path.abspath(os.path.join(harness_dir, ".."))
        process = subprocess.Popen(
            ['java', 'Harness'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=parent_dir
        )
        stdout, stderr = process.communicate(input=input_str)
        if stderr: return stderr.strip(), False
        return stdout.strip(), True
    except Exception as e: return str(e), False

def compile_java(harness_dir, solution_path):
    parent_dir = os.path.abspath(os.path.join(harness_dir, ".."))
    harness_path = os.path.join(harness_dir, "Harness.java")
    files = [solution_path, harness_path]
    result = subprocess.run(['javac', '-d', '.'] + files, capture_output=True, text=True, cwd=parent_dir)
    return result.returncode == 0, result.stderr

def test_student_code(solution_path, vm_tag="DEFAULT"):
    match = re.search(r'(.+)_(\d{8}_\d{6})', vm_tag)
    if match: username, timestamp = match.groups()
    else: username, timestamp = vm_tag, get_ist_time()

    slug = "java_digital_banking_system"
    report_base = f"/home/ubuntu/central_server/reports/{slug}/{username}"
    os.makedirs(report_base, exist_ok=True)
    report_path = os.path.join(report_base, f"{username}_{timestamp}.txt")

    harness_dir = os.path.dirname(os.path.abspath(__file__))
    success, err = compile_java(harness_dir, solution_path)
    if not success:
        with open(report_path, "w") as f: f.write(f"COMPILATION ERROR:\n{err}"); return

    test_cases = [
        { "name": "Savings Min Balance Failure", "input": "1\nSavings ACC01 1000 Withdraw 600", "expected": "Withdrawal Failed: Minimum balance requirement not met." },
        { "name": "Savings Valid Withdrawal", "input": "1\nSavings ACC01 1000 Withdraw 400", "expected": "Withdrawal Successful: New Balance: 600.0" },
        { "name": "Savings Deposit", "input": "1\nSavings ACC03 500 Deposit 500", "expected": "Deposit Successful: New Balance: 1000.0" },
        { "name": "Current Overdraft Success", "input": "1\nCurrent ACC02 100 Withdraw 1500", "expected": "Withdrawal Successful: New Balance: -1400.0" },
        { "name": "Current Overdraft Failure", "input": "1\nCurrent ACC02 100 Withdraw 3000", "expected": "Withdrawal Failed: Minimum balance requirement not met." },
        { "name": "Current Deposit", "input": "1\nCurrent ACC05 200 Deposit 800", "expected": "Deposit Successful: New Balance: 1000.0" },
        { "name": "Mixed Batch Success", "input": "2\nSavings ACC10 2000 Withdraw 1000\nCurrent ACC11 0 Withdraw 500", "expected": "Withdrawal Successful: New Balance: 1000.0\nWithdrawal Successful: New Balance: -500.0" },
        { "name": "Mixed Batch Failure", "input": "2\nSavings ACC20 500 Withdraw 100\nCurrent ACC21 -1500 Withdraw 600", "expected": "Withdrawal Failed: Minimum balance requirement not met.\nWithdrawal Failed: Minimum balance requirement not met." },
        { "name": "Zero Amount Transaction", "input": "2\nSavings ACC30 1000 Deposit 0\nCurrent ACC31 500 Withdraw 0", "expected": "Deposit Successful: New Balance: 1000.0\nWithdrawal Successful: New Balance: 500.0" },
        { "name": "Large Value Transaction", "input": "1\nCurrent ACC99 10000 Deposit 90000", "expected": "Deposit Successful: New Balance: 100000.0" }
    ]

    results = [f"Running Central Tests for: {slug}\n"]
    total_score = 0
    for i, tc in enumerate(test_cases, 1):
        actual, success = run_test(tc["input"] + "\n", harness_dir)
        expected_norm = "\n".join([l.strip().lower() for l in tc["expected"].splitlines()])
        actual_norm = "\n".join([l.strip().lower() for l in actual.splitlines()])
        
        if success and actual_norm == expected_norm:
            total_score += 3
            results.append(f"PASS TC{i:02d} (3/3)")
        else:
            results.append(f"FAIL TC{i:02d} (0/3)")

    results.append(f"\nTOTAL SCORE: {total_score}/30")
    with open(report_path, "w") as f: f.write("\n".join(results) + "\n")

if __name__ == "__main__":
    vm = sys.argv[1] if len(sys.argv) > 1 else "DEFAULT"
    sol = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "..", "student_workspace", "Solution.java")
    test_student_code(os.path.abspath(sol), vm)
