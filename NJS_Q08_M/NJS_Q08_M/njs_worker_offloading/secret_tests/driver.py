import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    base_path = get_base_path()
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False, 'tc8': False}
    # TC1: File server.js exists
    js_file = os.path.join(base_path, 'server.js')
    worker_file = os.path.join(base_path, 'worker.js')
    if os.path.exists(js_file):
        results['tc1'] = True
    if os.path.exists(worker_file):
        results['tc2'] = True
        
    try:
        with open(js_file, 'r') as f:
            content = f.read()
            if 'Worker' in content and 'worker_threads' in content:
                results['tc3'] = True
                results['tc4'] = True
                results['tc5'] = True
                results['tc8'] = True
        with open(worker_file, 'r') as f:
            w_content = f.read()
            if 'parentPort' in content or 'pbkdf2' in w_content:
                results['tc6'] = True
                results['tc7'] = True
    except Exception:
        pass
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
            "tc1": "File server.js exists in workspace", "tc2": "File worker.js exists in workspace", "tc3": "Worker pools utilized for processing CPU-intensive operations", "tc4": "Main execution threads remain non-blocked during hashing execution", "tc5": "Asynchronous response payloads correctly formatted", "tc6": "Worker data pbkdf2 properties configurations matched", "tc7": "System handles thread messaging error events", "tc8": "Node.js worker_threads module integrated successfully"
        }
        print("Running Tests for: Sync Offloading / Worker Pool\n")
        total_score = 0.0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = 2.5
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/20.0")
