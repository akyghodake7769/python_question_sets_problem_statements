import json
import os
import subprocess
import glob
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
            
        # TC1: Packaging is war
        if re.search(r'<packaging>\s*war\s*</packaging>', content):
            results['tc1'] = True
            
        # TC2: Tomcat scope provided
        if re.search(r'<artifactId>\s*spring-boot-starter-tomcat\s*</artifactId>[\s\S]*?<scope>\s*provided\s*</scope>', content):
            results['tc2'] = True
    except Exception:
        pass

    # TC3: Build executes without error
    try:
        process = subprocess.run(['mvn', 'clean', 'package'], cwd=base_path, capture_output=True, text=True)
        if process.returncode == 0:
            results['tc3'] = True
    except Exception:
        pass

    # TC4 & TC5: Check for war file in target
    try:
        target_dir = os.path.join(base_path, 'target')
        if os.path.exists(target_dir):
            war_files = glob.glob(os.path.join(target_dir, '*.war'))
            if war_files:
                results['tc4'] = True
                # Simple check for archive format
                if os.path.getsize(war_files[0]) > 100:
                    results['tc5'] = True
    except Exception:
        pass

    return results

if __name__ == "__main__":
    print(json.dumps(run_tests()))
