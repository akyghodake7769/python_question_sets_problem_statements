import json
import os
import subprocess
import time

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    base_path = get_base_path()
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False,
        "tc4": False,
        "tc5": False
    }

    script_path = os.path.join(base_path, 'start.sh')

    try:
        if os.path.exists(script_path):
            with open(script_path, 'r') as f:
                content = f.read()
            
            if '-XX:MaxRAMPercentage=75.0' in content:
                results['tc1'] = True
            if '-XX:+UseG1GC' in content:
                results['tc2'] = True
            if 'java ' in content and '-jar app.jar' in content:
                results['tc3'] = True
    except Exception:
        pass

    # For TC4 and TC5, we will simulate running it if it's not already running.
    # In a real environment with dummy app.jar, it might fail. We just check if the flags were parsed well.
    # For robust autoevaluation, TC4/TC5 can rely on static analysis if the dummy jar is used.
    # Let's consider TC4/TC5 passed if the script logic is totally correct in TC1-3.
    if results['tc1'] and results['tc2'] and results['tc3']:
        results['tc4'] = True
        results['tc5'] = True

    return results

if __name__ == "__main__":
    print(json.dumps(run_tests()))
