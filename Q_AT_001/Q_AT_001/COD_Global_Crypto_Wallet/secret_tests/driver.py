# import os
# import shutil
# import subprocess
# import re

# def test_student_code(solution_path):
#     # 1. Setup paths
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     report_path = os.path.join(os.path.dirname(solution_path), "report.txt")
    
#     # Target directory for the build (src/main/kotlin/Solution.kt)
#     build_dest = os.path.join(base_dir, "src", "main", "kotlin", "Solution.kt")
#     os.makedirs(os.path.dirname(build_dest), exist_ok=True)
    
#     # 2. Preparation: Copy student code to the testable location
#     shutil.copy(solution_path, build_dest)
    
#     print("-" * 65)
#     print(f"{'GLOBAL CRYPTO WALLET LLD AUDIT':^65}")
#     print("-" * 65)
#     report_lines = [
#         "-" * 65,
#         f"{'GLOBAL CRYPTO WALLET LLD AUDIT':^65}",
#         "-" * 65
#     ]
    
#     # 3. Execution: Run Gradle
#     try:
#         print("Warming up Gradle... (Initial run may take several minutes to download dependencies)\n")
#         # Determine the gradle executable and shell execution style
#         import platform
#         is_windows = platform.system().lower() == "windows"
#         shell_exec = True if is_windows else False
        
#         # 1. First, check if gradle is globally available in PATH
#         gradle_path = "gradle"
#         try:
#             check_res = subprocess.run([gradle_path, "--version"], capture_output=True, text=True, shell=shell_exec)
#             has_global_gradle = (check_res.returncode == 0)
#         except Exception:
#             has_global_gradle = False

#         if not has_global_gradle:
#             # 2. If not globally available, look in common locations
#             if is_windows:
#                 gradle_path = "C:/gradle-9.4.1/bin/gradle.bat"
#                 if not os.path.exists(gradle_path):
#                     home = os.path.expanduser("~")
#                     alt_path = os.path.join(home, "gradle-9.4.1", "bin", "gradle.bat").replace("\\", "/")
#                     if os.path.exists(alt_path):
#                         gradle_path = alt_path
#             else:
#                 # Ubuntu/Linux common paths
#                 linux_paths = [
#                     "/opt/gradle/gradle-9.4.1/bin/gradle",
#                     "/usr/bin/gradle",
#                     "/usr/local/bin/gradle"
#                 ]
#                 found_linux_path = False
#                 for lp in linux_paths:
#                     if os.path.exists(lp):
#                         gradle_path = lp
#                         found_linux_path = True
#                         break
#                 if not found_linux_path:
#                     # Fallback to home folder
#                     home = os.path.expanduser("~")
#                     alt_path = os.path.join(home, "gradle-9.4.1", "bin", "gradle")
#                     if os.path.exists(alt_path):
#                         gradle_path = alt_path

#         # Fix JAVA_HOME if it points to bin directory
#         env = os.environ.copy()
#         java_home = env.get("JAVA_HOME")
#         if java_home:
#             java_home_norm = java_home.replace("\\", "/").rstrip("/")
#             if java_home_norm.lower().endswith("/bin"):
#                 env["JAVA_HOME"] = java_home_norm[:-4]

#         result = subprocess.run([gradle_path, "cleanTest", "test"], capture_output=True, text=True, shell=shell_exec, cwd=base_dir, env=env)
        
#         # 4. Parsing (More granular parsing for 7 Test Cases)
#         total_score = 0
        
#         # Mapping markers from JUnit output
#         results_text = result.stdout + result.stderr
        
#         # DEBUG: If everything fails, print the output to see what's wrong
#         if "PASSED" not in results_text:
#             print("--- GRADLE DEBUG OUTPUT ---")
#             print(results_text)
#             print("--- END DEBUG OUTPUT ---")
        
#         test_mapping = {
#             "testInstantiation": ("TC1", "Instantiate complex structures", 0),
#             "testCreateWallet": ("TC2", "Add wallet with initial log", 1),
#             "testReceiveCrypto": ("TC3", "Receive with log tracking", 2),
#             "testSpendCrypto": ("TC4", "Spend with zero-balance logic", 3),
#             "testGetTransactionLog": ("TC5", "Retrieve full audit trail of wallet", 1),
#             "testTotalLiquidity": ("TC6", "Calculate total network liquidity", 1),
#             "testStakingRewards": ("TC7", "Perform bulk staking sweep", 2)
#         }
        
#         total_width = 70
#         for method, (tc_id, tc_desc, marks) in test_mapping.items():
#             # Check if the method name appears in the "passed" list of Gradle output
#             passed = f" > {method}() PASSED" in results_text
            
#             status_str = "[PASSED]" if passed else "[FAILED]"
#             tc_prefix = f"{tc_id}: {tc_desc} "
#             dot_count = max(2, total_width - len(tc_prefix))
#             dots = "." * dot_count
            
#             score_earned = marks if passed else 0
#             score_str = f"({score_earned}/{marks})"
            
#             msg = f"{tc_prefix}{dots} {status_str} {score_str}"
#             if passed:
#                 total_score += marks
            
#             print(msg)
#             report_lines.append(msg)
        
#         score_line = f"\n[SCORE] {total_score}"
#         print(score_line)
#         report_lines.append(score_line)
        
#         # 5. Output report
#         with open(report_path, "w", encoding="utf-8") as f:
#             f.write("\n".join(report_lines) + "\n")
            
#     except Exception as e:
#         print(f"Error during evaluation: {e}")

# if __name__ == "__main__":
#     # Point to the student's solution.kt
#     sol_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "student_workspace", "solution.kt")
#     test_student_code(sol_file)
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
    
    print("-" * 65)
    print(f"{'GLOBAL CRYPTO WALLET LLD AUDIT':^65}")
    print("-" * 65)
    report_lines = [
        "-" * 65,
        f"{'GLOBAL CRYPTO WALLET LLD AUDIT':^65}",
        "-" * 65
    ]
    
    # 3. Execution: Run Gradle
    try:
        print("Warming up Gradle... (Initial run may take several minutes to download dependencies)\n")
        # Determine the gradle executable and shell execution style
        import platform
        is_windows = platform.system().lower() == "windows"
        shell_exec = True if is_windows else False
        
        # 1. First, check if gradle is globally available in PATH
        gradle_path = shutil.which("gradle") or "gradle"
        has_global_gradle = False
        if gradle_path != "gradle":
            has_global_gradle = True
        else:
            try:
                check_res = subprocess.run([gradle_path, "--version"], capture_output=True, text=True, shell=shell_exec)
                has_global_gradle = (check_res.returncode == 0)
            except Exception:
                has_global_gradle = False

        if not has_global_gradle:
            # 2. If not globally available, look in common locations
            if is_windows:
                # Search standard C:/ and home locations
                candidate = "C:/gradle-9.4.1/bin/gradle.bat"
                found = False
                search_roots = ["C:/", os.path.expanduser("~")]
                for sr in search_roots:
                    if os.path.exists(sr):
                        try:
                            for entry in os.listdir(sr):
                                if "gradle" in entry.lower():
                                    p = os.path.join(sr, entry, "bin", "gradle.bat").replace("\\", "/")
                                    if os.path.exists(p):
                                        candidate = p
                                        found = True
                                        break
                        except Exception:
                            pass
                    if found:
                        break
                gradle_path = candidate
            else:
                # Ubuntu/Linux common paths
                linux_paths = [
                    "/opt/gradle/gradle-9.4.1/bin/gradle",
                    "/usr/bin/gradle",
                    "/usr/local/bin/gradle"
                ]
                # Scan common parent dirs for any gradle install
                scan_dirs = ["/opt", "/opt/gradle", "/usr", "/usr/local", "/usr/share", os.path.expanduser("~")]
                for sd in scan_dirs:
                    if os.path.exists(sd):
                        # check if it is directly bin/gradle
                        direct = os.path.join(sd, "bin", "gradle")
                        if os.path.exists(direct) and os.path.isfile(direct):
                            linux_paths.insert(0, direct)
                        # check subdirectories for bin/gradle
                        try:
                            for entry in os.listdir(sd):
                                if "gradle" in entry.lower():
                                    sub = os.path.join(sd, entry)
                                    if os.path.isdir(sub):
                                        p = os.path.join(sub, "bin", "gradle")
                                        if os.path.exists(p) and os.path.isfile(p):
                                            linux_paths.insert(0, p)
                        except Exception:
                            pass
                
                found_linux_path = False
                for lp in linux_paths:
                    if os.path.exists(lp):
                        gradle_path = lp
                        found_linux_path = True
                        break
                if not found_linux_path:
                    gradle_path = "gradle"

        # Fix JAVA_HOME if it points to bin directory
        env = os.environ.copy()
        java_home = env.get("JAVA_HOME")
        if java_home:
            java_home_norm = java_home.replace("\\", "/").rstrip("/")
            if java_home_norm.lower().endswith("/bin"):
                env["JAVA_HOME"] = java_home_norm[:-4]

        result = subprocess.run([gradle_path, "cleanTest", "test"], capture_output=True, text=True, shell=shell_exec, cwd=base_dir, env=env)
        
        # 4. Parsing (More granular parsing for 7 Test Cases)
        total_score = 0
        
        # Mapping markers from JUnit output
        results_text = result.stdout + result.stderr
        
        # DEBUG: If everything fails, print the output to see what's wrong
        if "PASSED" not in results_text:
            print("--- GRADLE DEBUG OUTPUT ---")
            print(results_text)
            print("--- END DEBUG OUTPUT ---")
        
        test_mapping = {
            "testInstantiation": ("TC1", "Instantiate complex structures", 0),
            "testCreateWallet": ("TC2", "Add wallet with initial log", 1),
            "testReceiveCrypto": ("TC3", "Receive with log tracking", 2),
            "testSpendCrypto": ("TC4", "Spend with zero-balance logic", 3),
            "testGetTransactionLog": ("TC5", "Retrieve full audit trail of wallet", 1),
            "testTotalLiquidity": ("TC6", "Calculate total network liquidity", 1),
            "testStakingRewards": ("TC7", "Perform bulk staking sweep", 2)
        }
        
        total_width = 70
        for method, (tc_id, tc_desc, marks) in test_mapping.items():
            # Check if the method name appears in the "passed" list of Gradle output
            passed = f" > {method}() PASSED" in results_text
            
            status_str = "[PASSED]" if passed else "[FAILED]"
            tc_prefix = f"{tc_id}: {tc_desc} "
            dot_count = max(2, total_width - len(tc_prefix))
            dots = "." * dot_count
            
            score_earned = marks if passed else 0
            score_str = f"({score_earned}/{marks})"
            
            msg = f"{tc_prefix}{dots} {status_str} {score_str}"
            if passed:
                total_score += marks
            
            print(msg)
            report_lines.append(msg)
        
        score_line = f"\n[SCORE] {total_score}"
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
