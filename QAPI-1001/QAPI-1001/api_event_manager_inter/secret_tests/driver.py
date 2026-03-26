import os
import sys
import importlib.util

def test_student_code(solution_path):
    run_tests(solution_path)

def run_tests(sol_p=None):
    base_p = os.path.dirname(os.path.abspath(__file__))
    if sol_p is None:
        sol_p = os.path.join(base_p, "..", "student_workspace", "solution.py")
    ref_p = os.path.join(base_p, "..", "student_workspace", "solution_reference.py")
    
    sys.path.append(os.path.join(base_p, "..", "student_workspace"))
    def lmod(n, p):
        s = importlib.util.spec_from_file_location(n, p)
        m = importlib.util.module_from_spec(s)
        s.loader.exec_module(m)
        return m

    print("Running Tests for: RESTful Event API Simulator (Intermediate)\n")
    try:
        sol = lmod("sol", sol_p); ref = lmod("ref", ref_p)
    except Exception as e:
        print(f"FAIL TC1 [Structure Check] (0/20) - Syntax: {e}"); return

    total = 0
    configs = [
        {"id": 1, "desc": "Verification of basic post", "marks": 0},
        {"id": 2, "desc": "Retrieve event with 404 logic", "marks": 3},
        {"id": 3, "desc": "Fully update event (PUT)", "marks": 3},
        {"id": 4, "desc": "Delete event resource", "marks": 3},
        {"id": 5, "desc": "Filter events by name substring (Search)", "marks": 3},
        {"id": 6, "desc": "Log filtering by level", "marks": 4},
        {"id": 7, "desc": "API usage statistics check", "marks": 4},
    ]

    for i, t in enumerate(configs, 1):
        try:
            r1, e1 = run_single(sol, ref, i)
            if compare_results(r1, e1):
                 print(f"PASS TC{i} [{t['desc']}] ({t['marks']}/{t['marks']})")
                 total += t["marks"]
            else:
                 print(f"FAIL TC{i} [{t['desc']}] (0/{t['marks']})")
        except Exception as ex:
             print(f"FAIL TC{i} [{t['desc']}] (0/{t['marks']}) - Error: {ex}")

    print(f"\nTotal Marks: {total}/20")

def run_single(mod, ref, tc):
    obj = mod.EventAPISimulator(); robj = ref.EventAPISimulator()
    obj.post_event(101, "API Lab"); robj.post_event(101, "API Lab")
    
    if tc == 1: return (True, True)
    if tc == 2:
        res1 = obj.get_event(101); ere1 = robj.get_event(101)
        res2 = obj.get_event(999); ere2 = robj.get_event(999)
        return ([res1, res2, obj.logs], [ere1, ere2, robj.logs])
    if tc == 3:
        res = obj.put_event(101, "New Title"); ere = robj.put_event(101, "New Title")
        return ([res, obj.events], [ere, robj.events])
    if tc == 4:
        obj.delete_event(101); robj.delete_event(101)
        return (obj.events, robj.events)
    if tc == 5:
        obj.post_event(102, "Cloud Workshop")
        robj.post_event(102, "Cloud Workshop")
        return (obj.search_events("cloud"), robj.search_events("cloud"))
    if tc == 6:
        obj.get_event(999); robj.get_event(999) # Generate WARNING
        return (obj.get_logs_by_level("WARNING"), robj.get_logs_by_level("WARNING"))
    if tc == 7: return (obj.get_api_usage_stats(), robj.get_api_usage_stats())
    return None

def compare_results(r, e):
    try:
        if isinstance(r, (float, int)): return round(float(r), 1) == round(float(e), 1)
        if isinstance(r, dict):
            if len(r) != len(e): return False
            for k in e:
                if k not in r: return False
                if not compare_results(r[k], e[k]): return False
            return True
        if isinstance(r, list):
            if len(r) != len(e): return False
            return all(compare_results(x, y) for x, y in zip(r, e))
        return str(r).strip() == str(e).strip()
    except: return False

if __name__ == "__main__":
    run_tests()
