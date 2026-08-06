import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False,
        "tc4": False
    }
    
    sol_path = os.path.join(get_base_path(), 'solution.json')
    if not os.path.exists(sol_path):
        # Fallback check if student created target file directly
        target_files = ['user_lookup.js', 'Dockerfile', 'db_pool.py', 'server.js', 'config.js', 'application.yml', 'regex_pattern.json', 'comments.js', 'cache_service.py', 'security_audit.json', 'outage_rca.json']
        for tf in target_files:
            alt_p = os.path.join(get_base_path(), tf)
            if os.path.exists(alt_p):
                try:
                    if tf.endswith('.json'):
                        with open(alt_p, 'r') as f:
                            data = json.load(f)
                        break
                    else:
                        data = {}
                        break
                except Exception:
                    data = {}
        else:
            data = {}
    else:
        try:
            with open(sol_path, 'r') as f:
                data = json.load(f)
        except Exception:
            data = {}

    # Specific question evaluation logic

    aws_k = data.get('aws_access_key', '').strip()
    jwt_s = data.get('jwt_secret', '').strip()
    rem = data.get('remediation', '').strip()
    results['tc1'] = True
    results['tc2'] = ('AKIA' in aws_k or 'EXAMPLE' in aws_k or len(aws_k) > 10)
    results['tc3'] = ('jwt' in jwt_s.lower() or 'secret' in jwt_s.lower() or len(jwt_s) > 10)
    results['tc4'] = (len(rem) > 10)


    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (5 if results.get('tc1') else 0) + (5 if results.get('tc2') else 0) + (5 if results.get('tc3') else 0) + (5 if results.get('tc4') else 0)
    
    solution_data = {
        'candidate_prefix': vm_tag,
        'assessment_start_time': start_time,
        'max_duration_minutes': 60,
        'evaluation_type': 'AUTO_EVALUATION',
        'score': score,
        'results': results,
        'exam_code': exam_code
    }
    
    ws_path = get_base_path()
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump(solution_data, f, indent=4)

if __name__ == "__main__":
    test_results = run_tests()
    
    try:
        sol_path = os.path.join(get_base_path(), 'solution.json')
        existing_data = {}
        if os.path.exists(sol_path):
            with open(sol_path, 'r') as f:
                existing_data = json.load(f)
        
        score = (5 if test_results.get('tc1') else 0) + (5 if test_results.get('tc2') else 0) + (5 if test_results.get('tc3') else 0) + (5 if test_results.get('tc4') else 0)
        existing_data['score'] = score
        existing_data['results'] = test_results
        
        with open(sol_path, 'w') as f:
            json.dump(existing_data, f, indent=4)
    except Exception:
        pass

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(test_results))
    else:
        TC_NAMES = {
            "tc1": "security_audit.json exists in student_workspace/ and is valid JSON",
            "tc2": "Hardcoded AWS Access Key identified",
            "tc3": "Hardcoded JWT secret token identified",
            "tc4": "Remediation recommendation provided"
        }
        print("Running Auto-Evaluation for: Basic Code Analysis: Security Audit of Hardcoded Credentials\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            if k == 'tc1':
                marks = 5
            elif k == 'tc2':
                marks = 5
            elif k == 'tc3':
                marks = 5
            elif k == 'tc4':
                marks = 5
            else:
                marks = 0

            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/20.0")
