import json
import os
import sys
import subprocess
from datetime import datetime, timezone, timedelta

# Global IST offset for consistent reporting
ist_offset = timezone(timedelta(hours=5, minutes=30))


def verify_task_central(username, start_time_str, exam_code="UNKNOWN", solution_path=None, labskraft_username=None):
    print(f"\n--- Central Validation for {username} ---")

    total_score = 0
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False}

    # Resolve solution.json path
    if not solution_path:
        solution_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'solution.json'))

    metadata = {}
    try:
        with open(solution_path, 'r') as f:
            metadata = json.load(f)
    except Exception:
        pass

    # Run the local driver.py to get fresh results
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(current_dir, 'driver.py')

    try:
        python_cmd = 'python3' if os.name != 'nt' else 'python'
        process = subprocess.run(
            [python_cmd, driver_path],
            capture_output=True,
            text=True,
            timeout=180
        )
        # driver.py prints the score report and saves solution.json — re-read it
        print(process.stdout)
        if process.stderr:
            print("[WARN]", process.stderr[:500])

        # Re-read updated solution.json
        try:
            with open(solution_path, 'r') as f:
                updated = json.load(f)
                results = updated.get('results', results)
                total_score = updated.get('score', 0)
                print("[SYSTEM] Successfully read updated results from solution.json.")
        except Exception:
            pass
    except Exception as e:
        print(f"[SYSTEM] Error running driver.py: {str(e)}")
        # Fall back to stored solution.json values
        results = metadata.get('results', results)
        total_score = metadata.get('score', 0)

    print(f"EXAM CODE: {exam_code}")

    tc_names = {
        'tc1': 'TC1 [Maven Compile]',
        'tc2': 'TC2 [Spring @Service Annotation]',
        'tc3': 'TC3 [Port 8081 Config]',
        'tc4': 'TC4 [App Running on Port 8081]',
        'tc5': 'TC5 [Actuator Health UP]',
    }

    tc_results = []
    for tc, name in tc_names.items():
        passed = results.get(tc, False)
        status = "PASSED" if passed else "FAILED"
        marks = 4 if passed else 0
        tc_results.append(f"{name} ({marks}/4)")
        print(f"{name} - {status}")

    print(f"TOTAL SCORE: {total_score}")

    date_str = datetime.now(ist_offset).strftime("%d-%m-%Y")
    time_str = datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")
    problem_code = "spring_boot_startup"

    tc_names_list = list(tc_names.values())
    tc_summary_str = f"{len(tc_names_list)}: {'; '.join(tc_names_list)}"

    csv_line = f"{date_str},{problem_code},{exam_code.upper()},{username},{time_str},{total_score},{tc_summary_str},0"
    print(f"\n[REPORT_CSV]{csv_line}")
    return total_score, results


if __name__ == '__main__':
    username = sys.argv[1] if len(sys.argv) > 1 else 'test_user'
    start_time_iso = sys.argv[2] if len(sys.argv) > 2 else datetime.now(timezone.utc).isoformat()
    exam_code = sys.argv[3] if len(sys.argv) > 3 else 'UNKNOWN'

    verify_task_central(username, start_time_iso, exam_code)
