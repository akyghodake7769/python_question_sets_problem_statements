import importlib.util
import os
import sys
import random

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return

    print("Running Tests for: Retail Inventory System (Randomized Anti-Cheat Mode)\n")
    report_lines = ["Running Tests for: Retail Inventory System (Randomized Anti-Cheat Mode)\n"]

    if not hasattr(solution, "RetailInventorySystem"):
        print("ERROR: RetailInventorySystem class not found"); return
    
    SystemClass = solution.RetailInventorySystem
    
    # 7 TCs: TC1(0), TC2(5), TC3(5), TC4(5), TC5(5), TC6(5), TC7(5) = 30
    tc_configs = [
        ("Initialize retail store structure", 0),
        ("Register a new product", 5),
        ("Update stock for existing item", 5),
        ("Process a sale with stock check", 5),
        ("Calculate total inventory value", 5),
        ("Handle multiple product registration", 5),
        ("Check consistency of large inventory", 5)
    ]

    random.seed(None)
    rv = random.randint(10, 100)
    rp = float(random.randint(100, 500))

    total_score = 0
    for i, (desc, marks) in enumerate(tc_configs, 1):
        try:
            def run_t(idx, name, price, stock):
                obj = SystemClass()
                if idx == 1: return obj.inventory
                if idx == 2: return obj.register_product(name, price, stock)
                if idx == 3: obj.register_product(name, price, stock); return obj.restock_item(name, 10)
                if idx == 4: obj.register_product(name, price, stock); return obj.complete_sale(name, 2)
                if idx == 5: obj.register_product(name, price, stock); return obj.inventory_report()
                if idx == 6: 
                    obj.register_product("A", 10.0, 10)
                    obj.register_product("B", 20.0, 5)
                    return len(obj.inventory)
                if idx == 7:
                    obj.register_product("X", price, stock)
                    obj.register_product("Y", 10.0, 10)
                    return obj.inventory_report()
                return None

            p_ok, h_det = False, False
            if i == 1:
                p_ok = (run_t(i, "", 0, 0) == {})
            else:
                # DUAL RUN
                res1 = run_t(i, "TestItem", 100.0, 10)
                res2 = run_t(i, "TestItem", rp, rv)
                
                if i == 2: exp2 = f"Product TestItem registered."
                elif i == 3: exp2 = f"Restocked TestItem. Now: {rv + 10}"
                elif i == 4: exp2 = f"Bill: ${rp * 2}"
                elif i == 5: exp2 = float(rp * rv)
                elif i == 6: exp2 = 2
                elif i == 7: exp2 = float(rp * rv + 100.0)

                if res1 == res2 and res2 != exp2: h_det = True
                elif res2 == exp2: p_ok = True

            if p_ok:
                total_score += marks
                msg = f"PASS TC{i} [{desc}] ({marks}/{marks})"
            elif h_det:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Hardcoded"
            else:
                msg = f"FAIL TC{i} [{desc}] (0/{marks})"
        except Exception as e: msg = f"FAIL TC{i} | Error: {e}"
        print(msg); report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/30.0"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
