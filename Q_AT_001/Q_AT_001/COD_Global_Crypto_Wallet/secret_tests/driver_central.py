import os
import sys
import shutil
import subprocess
import re
import traceback
from datetime import datetime, timezone, timedelta

def get_ist_time():
    try:
        ist = timezone(timedelta(hours=5, minutes=30))
        return datetime.now(ist).strftime("%Y%m%d_%H%M%S")
    except:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

def test_student_code(solution_path, vm_tag="DEFAULT"):
    # 1. Robust Path and Slug Discovery
    # User requested slug: Android_Track_Global_Crypto_Wallet
    slug = "Android_Track_Global_Crypto_Wallet"

    # 2. Report Path Resolution (Central Server Standard)
    match = re.search(r'(.+)_(\d{8}_\d{6})', vm_tag)
    if match:
        username, timestamp = match.groups()
    else:
        username, timestamp = vm_tag, get_ist_time()

    # Central Server Report Base
    report_base = f"/home/ubuntu/central_server/reports/{slug}/{username}"
    # Fallback for local testing (Windows)
    if os.name == 'nt':
        report_base = os.path.join(os.path.dirname(solution_path), "reports", username)
        
    os.makedirs(report_base, exist_ok=True)
    report_path = os.path.join(report_base, f"{username}_{timestamp}.txt")

    results = [f"Running Tests for: {slug} (Central Server - Android/Kotlin Mode)\n"]
    total_score = 0
    base_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        # 3. Validation: Check if student solution exists (.kt)
        abs_solution_path = os.path.abspath(solution_path)
        if not os.path.exists(abs_solution_path):
            raise FileNotFoundError(f"Solution file not found at {abs_solution_path}")

        # 4. Preparation: Copy student code to the Gradle testable location
        # Target: src/main/kotlin/Solution.kt
        build_dest = os.path.join(base_dir, "src", "main", "kotlin", "Solution.kt")
        os.makedirs(os.path.dirname(build_dest), exist_ok=True)
        shutil.copy(abs_solution_path, build_dest)

        # 5. Execution: Run Gradle test
        # We use --continue to run all tests even if some fail
        gradle_path = "C:/gradle-9.4.1/bin/gradle.bat"
        if not os.path.exists(gradle_path):
            user_profile = os.environ.get("USERPROFILE") or "C:/Users/nandi"
            alt_path = os.path.join(user_profile, "gradle-9.4.1", "bin", "gradle.bat").replace("\\", "/")
            if os.path.exists(alt_path):
                gradle_path = alt_path
        # Fix JAVA_HOME if it points to bin directory
        env = os.environ.copy()
        java_home = env.get("JAVA_HOME")
        if java_home:
            java_home_norm = java_home.replace("\\", "/").rstrip("/")
            if java_home_norm.lower().endswith("/bin"):
                env["JAVA_HOME"] = java_home_norm[:-4]

        result = subprocess.run([gradle_path, "test"], capture_output=True, text=True, shell=True, cwd=base_dir, env=env)
        results_text = result.stdout + result.stderr

        # 6. Test Case Configuration & Scoring (Mapping to the LLD Marks Table)
        tc_configs = [
            {"desc": "TC1: Instantiate complex structures", "method": "testCreateWallet", "m": 0},
            {"desc": "TC2: Add wallet with initial log", "method": "testCreateWallet", "m": 1},
            {"desc": "TC3: Receive with log tracking", "method": "testReceiveCrypto", "m": 2},
            {"desc": "TC4: Spend with zero-balance logic", "method": "testSpendCrypto", "m": 3},
            {"desc": "TC5: Retrieve full audit trail of wallet", "method": "testGetTransactionLog", "m": 1},
            {"desc": "TC6: Calculate total network liquidity", "method": "testTotalLiquidity", "m": 1},
            {"desc": "TC7: Perform bulk staking sweep", "method": "testStakingRewards", "m": 2}
        ]

        # 7. Parsing JUnit output for "PASSED" markers
        for idx, case in enumerate(tc_configs, 1):
            marks = float(case["m"])
            method = case["method"]
            desc = case["desc"]
            
            if f" > {method}() PASSED" in results_text:
                total_score += marks
                results.append(f"PASS TC{idx} [{desc}] ({marks}/{marks})")
            else:
                results.append(f"FAIL TC{idx} [{desc}] (0/{marks}) - Incorrect logic or compilation error.")

    except Exception as e:
        results.append(f"CRITICAL SYSTEM ERROR: {traceback.format_exc()}")

    # 8. Final Scoring Report
    results.append(f"\nSCORE: {total_score}/10 (Visible) | {total_score}/10 (Total)")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results) + "\n")
    
    print(f"✅ Report generated at: {report_path}")

if __name__ == "__main__":
    v_tag = sys.argv[1] if len(sys.argv) > 1 else "DEFAULT"
    s_path = sys.argv[2] if len(sys.argv) > 2 else "/home/ubuntu/submissions/solution.kt"
    test_student_code(s_path, v_tag)
