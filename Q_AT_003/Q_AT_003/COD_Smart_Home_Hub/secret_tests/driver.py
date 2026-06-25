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
    
    print("Running Tests for: Smart Home Hub (Intermediate LLD)\n")
    report_lines = ["Running Tests for: Smart Home Hub (Intermediate LLD)\n"]
    
    # 3. Execution: Run Gradle
    try:
        print("Warming up Gradle... (Initial run may take several minutes to download dependencies)\n")
        # Run gradle test (dynamically resolve based on OS and availability)
        if os.name == 'nt':
            local_gradle = r"C:\gradle-9.4.1\bin\gradle.bat"
            if os.path.exists(local_gradle):
                gradle_cmd = [local_gradle, "test"]
            else:
                gradle_cmd = "gradle test"
            use_shell = True
        else:
            gradle_cmd = ["gradle", "test"]
            use_shell = False
            
        result = subprocess.run(gradle_cmd, capture_output=True, text=True, shell=use_shell, cwd=base_dir)
        
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
            "testAddDevice": ("TC2 [Device Registration Logic]", 1.0),
            "testToggleDevice": ("TC3 [State Toggle Logic]", 2.0),
            "testScheduleTimer": ("TC4 [Scheduling with Constraints]", 3.0),
            "testGetDeviceHistory": ("TC5 [Audit Trail Retrieval]", 1.0),
            "testTotalPowerConsumption": ("TC6 [Network Power Summation]", 1.0),
            "testTurnOffAllDevices": ("TC7 [Bulk Power Sweep]", 2.0)
        }
        
        for method, (tc_name, marks) in test_mapping.items():
            # Check if the method name appears in the "passed" list of Gradle output
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
