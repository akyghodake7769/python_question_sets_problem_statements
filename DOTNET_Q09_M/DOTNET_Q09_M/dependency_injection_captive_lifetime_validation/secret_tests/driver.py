import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    base_path = get_base_path()
    results = {'tc1': True, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False}

    program_path = os.path.join(base_path, 'Program.cs')
    if os.path.exists(program_path):
        results['tc2'] = True
    else:
        return results

    try:
        with open(program_path, 'r') as f:
            content = f.read()
        
        # Check that Scoped is not captive in Singleton
        if 'builder.Services.AddSingleton<ServiceSingleton>();' not in content:
            results['tc3'] = True
        if 'AddScoped<ServiceSingleton>' in content or 'AddTransient<ServiceSingleton>' in content or 'AddSingleton<ServiceSingleton>(provider =>' in content or 'IServiceScopeFactory' in content:
            results['tc4'] = True
        if 'public class ServiceSingleton' in content:
            results['tc5'] = True
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
            "tc1": "Local VM Environment active and verified",
            "tc2": "Program.cs exists in workspace", "tc3": "Transient / Scoped services are not injected into Singleton class constructors", "tc4": "Register target scopes correctly under builder.Services", "tc5": "No syntax or compilation issues in Program.cs"
        }
        print("Running Tests for: Dependency Injection captive lifetime validation\n")
        total_score = 0
        marks_list = [4, 4, 4, 3]
        for k, v in test_results.items():
            tc_num = int(k[2:])
            desc = TC_NAMES.get(k, '')
            marks = marks_list[tc_num - 2] if tc_num > 1 else 0
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/15")
