import os
import sys
import importlib.util
import pandas as pd

def test_student_code(solution_path):
    run_tests(solution_path)

def run_tests(sol_p=None):
    base_p = os.path.dirname(os.path.abspath(__file__))
    if sol_p is None:
        sol_p = os.path.join(base_p, "..", "student_workspace", "solution.py")
    ref_p = os.path.join(base_p, "..", "student_workspace", "solution_reference.py")
    data_dir = os.path.join(base_p, "..", "data")
    stock_p = os.path.join(data_dir, "warehouse_stock.csv")
    logs_p = os.path.join(data_dir, "shipping_logs.csv")
    
    sys.path.append(os.path.join(base_p, "..", "student_workspace"))
    
    def lmod(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m

    print("Running Tests for: Supply Chain Optimizer\n")
    try:
        sol = lmod("sol", sol_p); ref = lmod("ref", ref_p)
    except Exception as e:
        print(f"FAIL TC1 [Structure Check] (0/20) - Syntax: {e}"); return

    tests = [
        {"id": 1, "desc": "Load internal DataFrames", "marks": 0},
        {"id": 2, "desc": "Verify Inner Join merging", "marks": 3},
        {"id": 3, "desc": "Filter sub-safety stock items", "marks": 3},
        {"id": 4, "desc": "Average transit days calculation", "marks": 3},
        {"id": 5, "desc": "Aggregate total financial value", "marks": 3},
        {"id": 6, "desc": "Grouped return rate analysis", "marks": 4},
        {"id": 7, "desc": "Multi-metric summary object", "marks": 4},
    ]

    total = 0
    for i, t in enumerate(tests, 1):
        desc = t["desc"]; marks = t["marks"]
        try:
            r1, e1 = run_single(sol, ref, i, stock_p, logs_p)
            if compare_results(r1, e1):
                print(f"PASS TC{i} [{desc}] ({marks}/{marks})"); total += marks
            else:
                 print(f"FAIL TC{i} [{desc}] (0/{marks}) - Incorrect Output.")
        except Exception as ex:
            print(f"FAIL TC{i} [{desc}] (0/{marks}) - Runtime Error: {ex}")
    
    print(f"\nTotal Marks: {total}/20")

def run_single(mod, ref, tc, stock_p, logs_p):
    mgr = mod.WarehouseManager(); opt = mod.SupplyOptimizer()
    rmgr = ref.WarehouseManager(); ropt = ref.SupplyOptimizer()
    
    if tc == 1:
        mgr.load_data(stock_p, logs_p); rmgr.load_data(stock_p, logs_p)
        return (isinstance(mgr.df_stock, pd.DataFrame), True)
    
    # Pre-loading for other tests to preserve independence
    df_s = pd.read_csv(stock_p); df_l = pd.read_csv(logs_p)
    
    if tc == 2:
        mgr.df_stock = df_s; mgr.df_logs = df_l
        rmgr.df_stock = df_s; rmgr.df_logs = df_l
        # Compare columns and row count
        m1 = mgr.get_merged_data(); m2 = rmgr.get_merged_data()
        return (len(m1), len(m2))

    if tc == 3: return (opt.get_at_risk_skus(df_s), ropt.get_at_risk_skus(df_s))
    if tc == 4: return (opt.calc_mean_lead_time(df_l), ropt.calc_mean_lead_time(df_l))
    if tc == 5: return (opt.total_inventory_value(df_s), ropt.total_inventory_value(df_s))
    if tc == 6: return (opt.carrier_return_rate(df_l), ropt.carrier_return_rate(df_l))
    if tc == 7:
        # MONKEY-PATCH for Independence: Substitute student's internal methods with reference
        opt.get_at_risk_skus = ropt.get_at_risk_skus
        opt.carrier_return_rate = ropt.carrier_return_rate
        return (opt.generate_summary(df_s, df_l), ropt.generate_summary(df_s, df_l))

    return (None, "NOT_IMPLEMENTED")

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
        return r == e
    except: return False

if __name__ == "__main__":
    run_tests()
