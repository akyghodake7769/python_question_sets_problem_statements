import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    base_path = get_base_path()
    results = {'tc1': False, 'tc2': False}
    # TC1: File server.js exists
    js_file = os.path.join(base_path, 'server.js')
    if os.path.exists(js_file):
        with open(js_file, 'r') as f:
            content = f.read()
            if 'uncaughtException' in content and 'unhandledRejection' in content:
                results['tc1'] = True
            if 'next' in content and 'app.use' in content:
                results['tc2'] = True
    return results

if __name__ == "__main__":
    test_results = run_tests()
    try:
        sol_path = os.path.join(get_base_path(), 'solution.java')
        with open(sol_path, 'w') as f:
            json.dump({'results': test_results}, f)
    except Exception:
        pass
    
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(test_results))
    else:
        TC_NAMES = {
            "tc1": "Global uncaughtException and unhandledRejection event listeners are registered", "tc2": "Application error boundaries route async exceptions safely"
        }
        print("Running Tests for: Express.js Exception Boundaries\n")
        total_score = 0.0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = 5
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/10.0")
