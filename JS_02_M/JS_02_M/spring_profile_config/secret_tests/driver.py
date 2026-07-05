import json
import os
import subprocess
import stat

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

    script_path = os.path.join(base_path, 'extract.sh')
    output_path = os.path.join(base_path, 'output.txt')

    # TC1: Check if script exists, has execution permissions, and runs
    try:
        if os.path.exists(script_path):
            st = os.stat(script_path)
            if bool(st.st_mode & stat.S_IXUSR):
                process = subprocess.run(['./extract.sh'], cwd=base_path, capture_output=True, timeout=5)
                if process.returncode == 0:
                    results['tc1'] = True
    except Exception:
        pass

    # Read output.txt for remaining TCs
    try:
        if os.path.exists(output_path):
            results['tc2'] = True
            with open(output_path, 'r') as f:
                content = f.read().strip()
            
            if content:
                results['tc3'] = True
                
            if 'prod_ultra_secure_pw_987!@#' in content:
                results['tc4'] = True
                
            if 'dev_super_secret_pw_123' not in content and 'default_password' not in content:
                results['tc5'] = True
    except Exception:
        pass

    return results

if __name__ == "__main__":
    print(json.dumps(run_tests()))
