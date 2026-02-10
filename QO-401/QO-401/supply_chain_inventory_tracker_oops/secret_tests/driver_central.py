import importlib.util
import os
import datetime
import pytz
from pathlib import Path
import inspect

IST = pytz.timezone("Asia/Kolkata")

def get_timestamp():
    return datetime.datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")

def test_student_code(solution_path, vm_tag):
    problem_code = "supply_chain_inventory_tracker_oops"
    base_dir = Path("/home/ubuntu/central_server")
    report_base_dir = base_dir / "reports" / problem_code / vm_tag
    os.makedirs(report_base_dir, exist_ok=True)

    timestamp = get_timestamp()
    report_file = report_base_dir / f"{vm_tag}_{timestamp}.txt"

    results = [f">> Testing solution for {vm_tag} at {timestamp}"]

    # Load student solution
    try:
        spec = importlib.util.spec_from_file_location("student_solution", solution_path)
        student_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student_module)
        results.append("solution.py loaded")
    except Exception as e:
        results.append(f"Failed to load SupplyChainInventory: {e}")
        _write_report(report_file, results)
        return

    results.append(f"\nRunning Tests for: Supply Chain Inventory Tracker\n")

    test_cases = [
        {
            "desc": "Add a new product to inventory",
            "func": "add_product",
            "setup": lambda: student_module.SupplyChainInventory(),
            "call": lambda obj: obj.add_product("PRD101", 50),
            "check": lambda result: isinstance(result, dict) and result.get("PRD101") == 50,
            "marks": 2.5
        },
        {
            "desc": "Fulfill an order by deducting stock",
            "func": "fulfill_order",
            "setup": lambda: (sc := student_module.SupplyChainInventory(), sc.add_product("PRD101", 50), sc)[0],
            "call": lambda obj: obj.fulfill_order("PRD101", 10),
            "check": lambda result: isinstance(result, dict) and result.get("PRD101") == 40,
            "marks": 2.5
        },
        {
            "desc": "Restock returned goods back into inventory",
            "func": "restock_return",
            "setup": lambda: (sc := student_module.SupplyChainInventory(), sc.add_product("PRD101", 50), sc.fulfill_order("PRD101", 10), sc)[0],
            "call": lambda obj: obj.restock_return("PRD101", 5),
            "check": lambda result: isinstance(result, dict) and result.get("PRD101") == 45,
            "marks": 2.5
        },
        {
            "desc": "List products with available stock",
            "func": "list_available_products",
            "setup": lambda: (sc := student_module.SupplyChainInventory(), sc.add_product("PRD101", 50), sc.add_product("PRD102", 0), sc)[0],
            "call": lambda obj: obj.list_available_products(),
            "check": lambda result: isinstance(result, list) and "PRD101" in result and "PRD102" not in result,
            "marks": 2.5
        },
        {
            "desc": "Update product stock when already exists",
            "func": "add_product",
            "setup": lambda: (sc := student_module.SupplyChainInventory(), sc.add_product("PRD101", 50), sc)[0],
            "call": lambda obj: obj.add_product("PRD101", 25),
            "check": lambda result: isinstance(result, dict) and result.get("PRD101") == 75,
            "marks": 2.5
        },
        {
            "desc": "Fulfill order with insufficient stock raises error",
            "func": "fulfill_order",
            "setup": lambda: (sc := student_module.SupplyChainInventory(), sc.add_product("PRD101", 10), sc)[0],
            "call": lambda obj: obj.fulfill_order("PRD101", 20),
            "check": lambda result: False,
            "should_raise": ValueError,
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Products with zero stock not listed",
            "func": "list_available_products",
            "setup": lambda: (sc := student_module.SupplyChainInventory(), sc.add_product("PRD101", 50), sc.add_product("PRD102", 10), sc.fulfill_order("PRD102", 10), sc)[0],
            "call": lambda obj: obj.list_available_products(),
            "check": lambda result: isinstance(result, list) and "PRD101" in result and "PRD102" not in result,
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Restock return for non-existent product creates entry",
            "func": "restock_return",
            "setup": lambda: student_module.SupplyChainInventory(),
            "call": lambda obj: obj.restock_return("PRD999", 15),
            "check": lambda result: isinstance(result, dict) and result.get("PRD999") == 15,
            "marks": 2.5,
            "is_hidden": True
        }
    ]

    total_score = 0
    max_score = 0
    visible_score = 0
    visible_max = 0
    hidden_score = 0
    hidden_max = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 2.5)
        is_hidden = case.get("is_hidden", False)
        max_score += marks
        
        if is_hidden:
            hidden_max += marks
        else:
            visible_max += marks
        
        try:
            obj = case["setup"]()
            
            func = getattr(obj, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()
            
            if 'pass' in src and len(src) < 80:
                msg = f"FAIL Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                results.append(msg)
                continue
            
            try:
                result = case["call"](obj)
                
                if case.get("should_raise"):
                    test_type = "Hidden" if is_hidden else "Visible"
                    msg = f"FAIL {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Expected {case['should_raise'].__name__} but no error raised"
                    results.append(msg)
                else:
                    passed = case["check"](result)
                    if passed:
                        test_type = "Hidden" if is_hidden else "Visible"
                        msg = f"PASS {test_type} Test Case {idx} Passed: {case['desc']}"
                        total_score += marks
                        if is_hidden:
                            hidden_score += marks
                        else:
                            visible_score += marks
                    else:
                        test_type = "Hidden" if is_hidden else "Visible"
                        msg = f"FAIL {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"
                    
                    results.append(msg)
            
            except Exception as e:
                if case.get("should_raise") and isinstance(e, case.get("should_raise")):
                    test_type = "Hidden" if is_hidden else "Visible"
                    msg = f"PASS {test_type} Test Case {idx} Passed: {case['desc']}"
                    total_score += marks
                    if is_hidden:
                        hidden_score += marks
                    else:
                        visible_score += marks
                    results.append(msg)
                else:
                    test_type = "Hidden" if is_hidden else "Visible"
                    msg = f"FAIL {test_type} Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"
                    results.append(msg)
        
        except Exception as e:
            test_type = "Hidden" if is_hidden else "Visible"
            msg = f"FAIL {test_type} Test Case {idx} Setup Error: {case['desc']} | Error: {str(e)}"
            results.append(msg)

    results.append(f"\nSCORE: {visible_score}/12.5 (Visible) + {hidden_score}/7.5 (Hidden) = {total_score}/20 (Total)")

    _write_report(report_file, results)

def _write_report(report_file, lines):
    with open(report_file, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python driver_central.py <vm_tag> [solution_path]")
        sys.exit(1)
    
    vm_tag = sys.argv[1]
    solution_path = sys.argv[2] if len(sys.argv) > 2 else "/home/ubuntu/submissions/solution.py"
    test_student_code(solution_path, vm_tag)
