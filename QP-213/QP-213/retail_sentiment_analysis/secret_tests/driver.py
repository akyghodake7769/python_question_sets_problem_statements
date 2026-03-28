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
    ref_p = os.path.join(base_p, "..", "student_workspace", "solution.py")
    data_dir = os.path.join(base_p, "..", "data")
    sales_p = os.path.join(data_dir, "product_sales.csv")
    reviews_p = os.path.join(data_dir, "customer_reviews.csv")
    
    sys.path.append(os.path.join(base_p, "..", "student_workspace"))
    
    def lmod(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m

    print("Running Tests for: Retail Sentiment Analysis\n")
    try:
        sol = lmod("sol", sol_p); ref = lmod("ref", ref_p)
    except Exception as e:
        print(f"FAIL TC1 [Structure Check] (0/20) - Syntax: {e}"); return

    tests = [
        {"id": 1, "desc": "Load internal DataFrames", "marks": 0},
        {"id": 2, "desc": "Filter sales by volume threshold", "marks": 3},
        {"id": 3, "desc": "Categorical price aggregation", "marks": 3},
        {"id": 4, "desc": "Product-level review aggregation", "marks": 3},
        {"id": 5, "desc": "Cross-dataset merging check", "marks": 3},
        {"id": 6, "desc": "Discount/Sales impact analysis", "marks": 4},
        {"id": 7, "desc": "Opportunity detection logic", "marks": 4},
    ]

    total = 0
    df_s = pd.read_csv(sales_p); df_r = pd.read_csv(reviews_p)

    for i, t in enumerate(tests, 1):
        desc = t["desc"]; marks = t["marks"]
        try:
            r1, e1 = run_single(sol, ref, i, df_s, df_r, sales_p, reviews_p)
            if compare_results(r1, e1):
                print(f"PASS TC{i} [{desc}] ({marks}/{marks})"); total += marks
            else:
                 print(f"FAIL TC{i} [{desc}] (0/{marks}) - Incorrect Output.")
        except Exception as ex:
            print(f"FAIL TC{i} [{desc}] (0/{marks}) - Runtime Error: {ex}")
    
    print(f"\nTotal Marks: {total}/20")

def run_single(mod, ref, tc, df_s, df_r, s_p, r_p):
    st = mod.SalesTracker(); sa = mod.SentimentAnalyzer()
    rst = ref.SalesTracker(); rsa = ref.SentimentAnalyzer()
    
    if tc == 1:
        st.load_csvs(s_p, r_p); rst.load_csvs(s_p, r_p)
        return (isinstance(st.df_sales, pd.DataFrame), True)
    
    if tc == 2:
        st.df_sales = df_s; rst.df_sales = df_s
        return (len(st.get_top_sellers(100)), len(rst.get_top_sellers(100)))

    if tc == 3:
        st.df_sales = df_s; rst.df_sales = df_s
        return (st.category_price_analysis().to_dict(), rst.category_price_analysis().to_dict())

    if tc == 4:
        # Use orient='records' for easier comparison of DataFrames as list of dicts
        d1 = sa.aggregate_reviews(df_r).to_dict(orient='records')
        d2 = rsa.aggregate_reviews(df_r).to_dict(orient='records')
        return (d1, d2)
    
    if tc == 5: 
        # MONKEY-PATCH for Independence: Substitute student's aggregation with reference
        sa.aggregate_reviews = rsa.aggregate_reviews 
        return (len(sa.get_correlation_summary(df_s, df_r)), len(rsa.get_correlation_summary(df_s, df_r)))
    
    if tc == 6: return (sa.discount_performance(df_s), rsa.discount_performance(df_s))
    
    if tc == 7:
        m = rsa.get_correlation_summary(df_s, df_r)
        return (sa.detect_opportunities(m), rsa.detect_opportunities(m))

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
