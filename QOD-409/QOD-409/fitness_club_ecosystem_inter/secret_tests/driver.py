import importlib.util
import os
import sys
import random

def test_student_code(solution_path):
    report_dir = os.path.dirname(solution_path)
    report_path = os.path.join(report_dir, "report.txt")
    
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return

    print("Running Tests for: Fitness Club Ecosystem (Enriched QO-420 Mode)\n")
    report_lines = ["Running Tests for: Fitness Club Ecosystem (Enriched QO-420 Mode)\n"]

    if not hasattr(solution, "ClubRegistry"):
        print("ERROR: ClubRegistry class not found"); return
    
    RegistryClass = solution.ClubRegistry
    
    tc_configs = [
        ("Verification of registry initialization", 0),
        ("Registering a valid profile", 1),
        ("Verification of tiered zone access", 1),
        ("Scheduling unique workout slots", 1),
        ("Membership tier upgrade logic", 1),
        ("Logging attendance record", 1),
        ("Membership + trainer fees", 2.5),
        ("Member engagement analytics", 2.5)
    ]

    random.seed(None)

    total_score = 0
    for i, (desc, marks) in enumerate(tc_configs, 1):
        try:
            def run_t(idx, current_obj, params):
                name, t, z = params
                if idx == 1: 
                    t1 = RegistryClass()
                    if not hasattr(t1, 'members'): return "MISSING_ATTR"
                    return t1.members
                
                if idx == 2: current_obj.add_member(name, t); return name in current_obj.members
                if idx == 3: return current_obj.can_access_zone(name, z)
                if idx == 4: return current_obj.schedule_session(name, "2024-01-01", "10:00", "Coach-X")
                if idx == 5: return current_obj.upgrade_tier(name, "VIP")
                if idx == 6: return current_obj.mark_attendance(name, "2024-01-01", "10:00")
                if idx == 7: return current_obj.get_monthly_fee(name)
                if idx == 8: return current_obj.get_member_stats(name)
                return None

            p_ok, h_det, none_ret = False, False, False
            actual_res = None
            expected_res = None

            if i == 1:
                actual_res = run_t(i, None, ("", "", ""))
                expected_res = {}
                p_ok = (actual_res == expected_res)
            else:
                d1 = ("Alice", "Standard", "Gym_Floor")
                d2 = ("Bob", "Premium", "Pool")
                
                # RUN 1
                obj1 = RegistryClass(); obj1.add_member(*d1[:2])
                res1 = run_t(i, obj1, d1)
                
                # RUN 2
                obj2 = RegistryClass(); obj2.add_member(*d2[:2])
                res2 = run_t(i, obj2, d2)
                
                actual_res = res1
                def get_ref(idx, name, t, z):
                    if idx == 2: return True
                    if idx == 3: return True
                    if idx == 4: return True
                    if idx == 5: return True
                    if idx == 6: 
                        # mark_attendance needs a session first. 
                        # run_t(4) is NOT called here. We need to manually add it or call run_t in sequence.
                        # Wait, Independence means we should handle state injection.
                        pass
                    if idx == 7: return 40.0 # No sessions yet
                    if idx == 8: return {'total_sessions': 0, 'attendance_rate': 0.0}
                    return None

                # For complex methods, I'll inject state inside the check block
                if i in [6, 7, 8]:
                    obj1.schedule_session("Alice", "2024-01-01", "10:00", "X")
                    if i >= 6: 
                        # Re-run for RUN 1
                        res1 = run_t(i, obj1, d1)
                        actual_res = res1
                    
                    obj2.schedule_session("Bob", "2024-01-01", "10:00", "X")
                    res2 = run_t(i, obj2, d2)

                    if i == 6: expected_res = True
                    if i == 7: expected_res = 40.0 + 20.0
                    if i == 8: 
                        obj1.mark_attendance("Alice", "2024-01-01", "10:00")
                        obj2.mark_attendance("Bob", "2024-01-01", "10:00")
                        res1 = run_t(i, obj1, d1)
                        res2 = run_t(i, obj2, d2)
                        actual_res = res1
                        expected_res = {'total_sessions': 1, 'attendance_rate': 100.0}
                else:
                    expected_res = get_ref(i, *d1) if i != 6 else True

                if actual_res == expected_res:
                    def get_ref2(idx, name, t, z):
                        if idx == 2: return True
                        if idx == 3: return True
                        if idx == 4: return True
                        if idx == 5: return True
                        if idx == 6: return True
                        if idx == 7: return 80.0 + 20.0
                        if idx == 8: return {'total_sessions': 1, 'attendance_rate': 100.0}
                    if res2 == get_ref2(i, *d2): p_ok = True
                    else: h_det = True
                elif actual_res is None: none_ret = True
                elif res1 == res2:
                    if i not in [2, 4, 5, 6]: h_det = True

            if p_ok:
                total_score += marks
                msg = f"PASS TC{i} [{desc}] ({marks}/{marks})"
            elif none_ret:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Method not implemented / No return value"
            elif h_det:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Hardcoded result detected."
            else:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Incorrect Output. Expected: {expected_res} | Actual: {actual_res}"
        except Exception as e: msg = f"FAIL TC{i} [{desc}] | Error: {e}"
        print(msg); report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/10"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    import sys
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
