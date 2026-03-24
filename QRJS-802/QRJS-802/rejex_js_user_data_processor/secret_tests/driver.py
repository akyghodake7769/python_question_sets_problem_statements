import sys
import os
import importlib.util

base_p = os.path.dirname(os.path.abspath(__file__))
parent_p = os.path.dirname(base_p)
sys.path.append(os.path.join(parent_p, 'student_workspace'))

def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def run_tests():
    sol_p = os.path.join(parent_p, 'student_workspace', 'solution.py')
    ref_p = os.path.join(parent_p, 'student_workspace', 'solution_reference.py')
    try:
        sol = load_mod("solution", sol_p); ref = load_mod("solution_reference", ref_p)
    except Exception as e:
        print(f"FAIL TC1 [Structure Check] (0/25) - Syntax: {e}"); return

    tests = [
        {"id": 1, "desc": "Initialize UserDataProcessor", "marks": 0},
        {"id": 2, "desc": "Validate email addresses (Regex)", "marks": 4},
        {"id": 3, "desc": "Validate username (5-10 alphanumeric)", "marks": 4},
        {"id": 4, "desc": "Clean phone string (Digits only)", "marks": 4},
        {"id": 5, "desc": "Format dict to JSON (Indent=4)", "marks": 4},
        {"id": 6, "desc": "Parse JSON string to dict", "marks": 4},
        {"id": 7, "desc": "Mask email for privacy", "marks": 5},
    ]

    total = 0
    for i, t in enumerate(tests, 1):
        desc = t["desc"]; marks = t["marks"]
        try:
            r1, e1 = run_s(sol, ref, i, "FIXED")
            r2, e2 = run_s(sol, ref, i, "RANDOM")
            if r1 == e1 and r2 == e2:
                print(f"PASS TC{i} [{desc}] ({marks}/{marks})"); total += marks
            elif r1 == "NOT_IMPLEMENTED":
                 print(f"FAIL TC{i} [{desc}] (0/{marks}) - Method code missing")
            else:
                 print(f"FAIL TC{i} [{desc}] (0/{marks}) - Incorrect Output. Exp: {e1} | Act: {r1}")
        except Exception as ex:
            print(f"FAIL TC{i} [{desc}] (0/{marks}) - Runtime: {ex}")
    print(f"\nTotal Marks: {total}/25")

def run_s(mod, ref, tc, mode):
    proc = mod.UserDataProcessor(); rproc = ref.UserDataProcessor()
    if tc == 1: return (type(proc), type(rproc))
    
    if tc == 2:
        em = "test@example.com" if mode == "FIXED" else "err-email"
        return (proc.validate_email(em), rproc.validate_email(em))

    if tc == 3:
        un = "user123" if mode == "FIXED" else "short"
        return (proc.validate_username(un), rproc.validate_username(un))

    if tc == 4:
        ph = "+1 (555) 123-4567" if mode == "FIXED" else "abc-999-def"
        return (proc.clean_phone(ph), rproc.clean_phone(ph))

    if tc == 5:
        d = {"a": 1} if mode == "FIXED" else {"x": 100, "y": 200}
        return (proc.to_json(d), rproc.to_json(d))

    if tc == 6:
        j = '{"status": "ok"}' if mode == "FIXED" else '{"id": 1, "val": 22}'
        return (proc.from_json(j), rproc.from_json(j))

    if tc == 7:
        em = "jack.sparrow@pirate.com" if mode == "FIXED" else "me@home.net"
        return (proc.mask_email(em), rproc.mask_email(em))

    return (None, "NOT_IMPLEMENTED")

if __name__ == "__main__":
    run_tests()
