import sys
import json
import os
import subprocess
import re

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

    pom_path = os.path.join(base_path, 'pom.xml')
    
    try:
        with open(pom_path, 'r') as f:
            content = f.read()
            
        # TC1: POM has been modified to include exclusion
        if '<exclusion>' in content or '<exclusions>' in content:
            results['tc1'] = True
            
        # TC2: Exclusion is for guava
        if re.search(r'<exclusion>[\s\S]*?<groupId>\s*com\.google\.guava\s*</groupId>[\s\S]*?<artifactId>\s*guava\s*</artifactId>[\s\S]*?</exclusion>', content):
            results['tc2'] = True
    except Exception:
        pass

    # TC3 & TC4: Maven tasks
    try:
        # Compile
        compile_proc = subprocess.run(['mvn', 'clean', 'compile'], cwd=base_path, capture_output=True, text=True)
        if compile_proc.returncode == 0:
            results['tc4'] = True
            
        # Dependency tree (check if old guava is excluded)
        tree_proc = subprocess.run(['mvn', 'dependency:tree'], cwd=base_path, capture_output=True, text=True)
        if tree_proc.returncode == 0:
            # If guava is excluded from hadoop, the only guava should be the top-level 32.1.3
            if 'guava:20' not in tree_proc.stdout and 'guava:27' not in tree_proc.stdout:
                results['tc3'] = True
    except Exception:
        pass

    # TC5: Simulated run successful (If it compiles and no conflict, it passes)
    if results['tc2'] and results['tc4']:
        results['tc5'] = True

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
            "tc1": "POM modified to include exclusion",
            "tc2": "Exclusion targets Guava dependency",
            "tc3": "Maven tasks execute successfully",
            "tc4": "Dependency tree resolves correctly",
            "tc5": "Simulated run successful"
        }
        print("Running Tests for: Maven Dependency Conflict\n")
        total_score = 0
        for k, v in test_results.items():
            if k.lower().startswith('tc'):
                tc_num = k[2:]
                desc = TC_NAMES.get(k.lower(), '')
                if v:
                    total_score += 4
                    print(f"PASS TC{tc_num} [{desc}] (4/4)")
                else:
                    print(f"FAIL TC{tc_num} [{desc}] (0/4)")
        print(f"\nSCORE: {total_score}/20.0")
