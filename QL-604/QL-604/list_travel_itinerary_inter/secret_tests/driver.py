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

    print("Running Tests for: Travel Itinerary Planner (Enriched QO-420 Mode)\n")
    report_lines = ["Running Tests for: Travel Itinerary Planner (Enriched QO-420 Mode)\n"]

    if not hasattr(solution, "ItineraryPlanner"):
        print("ERROR: ItineraryPlanner class not found"); return
    
    PlannerClass = solution.ItineraryPlanner
    
    tc_configs = [
        ("Verification of list initialization", 0),
        ("Strategic adding of new destination", 1),
        ("Number of unique stops in the plan", 1),
        ("Finding the index of a specific stop", 1),
        ("Removing a valid destination", 1),
        ("Reversed itinerary in uppercase", 2),
        ("Detecting identical city names", 2),
        ("Formatting string with stop count", 2)
    ]

    random.seed(None)

    total_score = 0
    for i, (desc, marks) in enumerate(tc_configs, 1):
        try:
            def run_t(idx, current_obj, data_params):
                cities = data_params
                if idx == 1: 
                    t1 = PlannerClass(cities)
                    if not hasattr(t1, 'destinations'): return "MISSING_ATTR"
                    return t1.destinations
                
                if idx == 2: return current_obj.add_destination(cities[0])
                if idx == 3: return current_obj.get_total_stops()
                if idx == 4: return current_obj.get_stop_index(cities[1])
                if idx == 5: return current_obj.remove_destination(cities[0])
                if idx == 6: return current_obj.get_reversed_itinerary()
                if idx == 7: return current_obj.has_duplicates()
                if idx == 8: return current_obj.format_itinerary()
                return None

            p_ok, h_det, none_ret = False, False, False
            actual_res = None
            expected_res = None

            if i == 1:
                test_data = ["London", "Paris"]
                actual_res = run_t(i, None, test_data)
                expected_res = list(test_data)
                p_ok = (actual_res == expected_res)
            else:
                d1 = ["Paris", "London", "Rome", "Paris"]
                d2 = ["Tokyo", "Berlin", "Osaka", "Miami"]
                
                # RUN 1
                obj1 = PlannerClass([]); obj1.destinations = list(d1)
                res1 = run_t(idx=i, current_obj=obj1, data_params=d1)
                
                # RUN 2
                obj2 = PlannerClass([]); obj2.destinations = list(d2)
                res2 = run_t(idx=i, current_obj=obj2, data_params=d2)
                
                actual_res = res1
                # Reference logic for RUN 1
                def get_ref(idx, data):
                    if idx == 2: 
                        # Strategic add: Paris is already at end? No, London.
                        # Wait, d1 ends in Paris. If we add "Paris" -> False. 
                        # But run_t for idx 2 adds data[0] -> "Paris".
                        # d1 is ["Paris", "London", "Rome", "Paris"]. 
                        # Adding data[0] ("Paris") to obj with d1 -> Already ends in Paris?
                        # Yes! So it should return False.
                        return False
                    if idx == 3: return len(set(data))
                    if idx == 4: return 1 # Index of data[1] ("London")
                    if idx == 5: return True # Remove data[0] ("Paris")
                    if idx == 6: return [c.upper() for c in data[::-1]]
                    if idx == 7: return len(data) != len(set(data))
                    if idx == 8: return " -> ".join(data) + f" ({len(data)} stops)"
                    return None

                expected_res = get_ref(i, d1)

                if actual_res == expected_res:
                    def get_ref2(idx, data):
                        if idx == 2: return True
                        if idx == 3: return len(set(data))
                        if idx == 4: return 1
                        if idx == 5: return True
                        if idx == 6: return [c.upper() for c in data[::-1]]
                        if idx == 7: return len(data) != len(set(data))
                        if idx == 8: return " -> ".join(data) + f" ({len(data)} stops)"
                        return None
                    
                    if res2 == get_ref2(i, d2):
                        p_ok = True
                    else:
                        h_det = True
                elif actual_res is None:
                    none_ret = True
                elif res1 == res2:
                    h_det = True

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
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
