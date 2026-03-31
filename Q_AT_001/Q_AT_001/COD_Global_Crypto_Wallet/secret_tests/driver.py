import os
import shutil
import subprocess
import re

def test_student_code(solution_path):
    # 1. Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(os.path.dirname(solution_path), "report.txt")
    
    # Target directory for the build (src/main/kotlin/Solution.kt)
    build_dest = os.path.join(base_dir, "src", "main", "kotlin", "Solution.kt")
    os.makedirs(os.path.dirname(build_dest), exist_ok=True)
    
    # 2. Preparation: Copy student code to the testable location
    shutil.copy(solution_path, build_dest)
    
    print("Running Tests for: Global Crypto Wallet (Intermediate LLD)\n")
    report_lines = ["Running Tests for: Global Crypto Wallet (Intermediate LLD)\n"]
    
    # 3. Execution: Run Gradle
    try:
        # Run gradle test
        result = subprocess.run(["gradle", "test"], capture_output=True, text=True, shell=True, cwd=base_dir)
        
        # 4. Parsing (More granular parsing for 7 Test Cases)
        total_score = 0.0
        
        # Mapping markers from JUnit output or parsing the test results file
        results_text = result.stdout + result.stderr
        
        test_mapping = {
            "testCreateWallet": ("TC2 [Account Registration Logic]", 1.0),
            "testReceiveCrypto": ("TC3 [Secure Deposit/Receive Logic]", 2.0),
            "testSpendCrypto": ("TC4 [Withdrawal/Spend Overdraft Logic]", 3.0),
            "testGetTransactionLog": ("TC5 [Audit Trail Retrieval]", 1.0),
            "testTotalLiquidity": ("TC6 [Network Liquidity Summation]", 1.0),
            "testStakingRewards": ("TC7 [Bulk Interest/Reward Sweep]", 2.0)
        }
        
        for method, (tc_name, marks) in test_mapping.items():
            # Check if the method name appears in the "passed" list of Gradle output
            # (Note: This is a simplified parser; in real scenarios, we'd parse the XML report)
            if f" > {method}() PASSED" in results_text:
                msg = f"PASS {tc_name} ({marks}/{marks})"
                total_score += marks
            else:
                msg = f"FAIL {tc_name} (0/{marks})"
            
            print(msg)
            report_lines.append(msg)
        
        score_line = f"\nTOTAL SCORE: {total_score}/10.0"
        print(score_line)
        report_lines.append(score_line)
        
        # 5. Output report
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
            
    except Exception as e:
        print(f"Error during evaluation: {e}")

if __name__ == "__main__":
    # Point to the student's solution.kt
    sol_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "student_workspace", "solution.kt")
    test_student_code(sol_file)
