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
        print("Warming up Gradle... (Initial run may take several minutes to download dependencies)\n")
        # Determine the gradle executable and shell execution style
        import platform
        is_windows = platform.system().lower() == "windows"
        shell_exec = True if is_windows else False
        
        # 1. First, check if gradle is globally available in PATH
        gradle_path = "gradle"
        try:
            subprocess.run([gradle_path, "--version"], capture_output=True, text=True, shell=shell_exec)
            has_global_gradle = True
        except Exception:
            has_global_gradle = False

        if not has_global_gradle:
            # 2. If not globally available, look in common locations
            if is_windows:
                gradle_path = "C:/gradle-9.4.1/bin/gradle.bat"
                if not os.path.exists(gradle_path):
                    user_profile = os.environ.get("USERPROFILE") or "C:/Users/nandi"
                    alt_path = os.path.join(user_profile, "gradle-9.4.1", "bin", "gradle.bat").replace("\\", "/")
                    if os.path.exists(alt_path):
                        gradle_path = alt_path
            else:
                # Ubuntu/Linux common paths
                linux_paths = [
                    "/opt/gradle/gradle-9.4.1/bin/gradle",
                    "/usr/bin/gradle",
                    "/usr/local/bin/gradle"
                ]
                found_linux_path = False
                for lp in linux_paths:
                    if os.path.exists(lp):
                        gradle_path = lp
                        found_linux_path = True
                        break
                if not found_linux_path:
                    # Fallback to home folder
                    home = os.environ.get("HOME") or "/home/ubuntu"
                    alt_path = os.path.join(home, "gradle-9.4.1", "bin", "gradle")
                    if os.path.exists(alt_path):
                        gradle_path = alt_path

        # Fix JAVA_HOME if it points to bin directory
        env = os.environ.copy()
        java_home = env.get("JAVA_HOME")
        if java_home:
            java_home_norm = java_home.replace("\\", "/").rstrip("/")
            if java_home_norm.lower().endswith("/bin"):
                env["JAVA_HOME"] = java_home_norm[:-4]

        result = subprocess.run([gradle_path, "test"], capture_output=True, text=True, shell=shell_exec, cwd=base_dir, env=env)
        
        # 4. Parsing (More granular parsing for 7 Test Cases)
        total_score = 0.0
        
        # Mapping markers from JUnit output
        results_text = result.stdout + result.stderr
        
        # DEBUG: If everything fails, print the output to see what's wrong
        if "PASSED" not in results_text:
            print("--- GRADLE DEBUG OUTPUT ---")
            print(results_text)
            print("--- END DEBUG OUTPUT ---")
        
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
