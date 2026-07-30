import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def print_separator():
    print("-" * 70)

def print_test_case(name, status, score, max_score, reason):
    pad_length = 63 - len(name) - 1
    if pad_length < 1: 
        pad_length = 1
    dots = "." * pad_length
    print(f"{name} {dots} {status} ({score}/{max_score})")
    print(f"    └─ [Reason]: {reason}")

def verify_task():
    if sys.platform.startswith('win'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    cand_username = os.getenv("LABSKRAFT_USERNAME") or os.getenv("DATABRICKS_USERNAME")
    exam_code = os.getenv("KODEBUCK_EXAM_CODE") or os.getenv("EXAM_CODE") or "UNKNOWN"
    
    sol_path = os.path.join(get_base_path(), 'solution.json')
    if os.path.exists(sol_path):
        try:
            with open(sol_path, 'r') as f:
                data = json.load(f)
            if data.get('labskraft_username'):
                cand_username = data['labskraft_username']
            if data.get('exam_code'):
                exam_code = data['exam_code']
        except Exception:
            pass

    # Normalize candidate username
    cand_normalized = None
    if cand_username:
        raw_cand = cand_username
        if '@' in raw_cand:
            raw_cand = raw_cand.split('@')[0]
        if '_' in raw_cand:
            raw_cand = raw_cand.split('_')[0]
        cand_normalized = raw_cand.lower().replace('.', '-')

    # Normalize system OS username
    sys_username = os.getenv("username") or os.getenv("USER") or "student"
    raw_sys = sys_username
    if '@' in raw_sys:
        raw_sys = raw_sys.split('@')[0]
    if '_' in raw_sys:
        raw_sys = raw_sys.split('_')[0]
    sys_normalized = raw_sys.lower().replace('.', '-')

    # Build variations
    catalog_variations = []
    for u in [cand_normalized, sys_normalized]:
        if not u:
            continue
        if exam_code and exam_code != "UNKNOWN":
            catalog_variations.append(f"ut_ltm_{u}_{exam_code.lower()}".lower().replace('-', '_'))
            catalog_variations.append(f"ut_ltm_{u}-{exam_code.lower()}".lower().replace('-', '_'))
        catalog_variations.append(f"ut_ltm_{u}".lower().replace('-', '_'))
    
    catalog_variations = list(dict.fromkeys(catalog_variations))
    expected_catalog_name = catalog_variations[0]

    total_score = 0
    max_score = 20
    
    catalog_exists = False
    schema_exists = False
    table_exists = False
    structure_valid = False
    format_valid = False
    
    client = None
    init_error = None
    
    # 1. Connect to Databricks
    try:
        from databricks.sdk import WorkspaceClient
        host = os.getenv("DATABRICKS_HOST")
        token = os.getenv("DATABRICKS_TOKEN")
        if not host or not token:
            missing = []
            if not host: missing.append("DATABRICKS_HOST")
            if not token: missing.append("DATABRICKS_TOKEN")
            raise ValueError(f"Missing environment variable(s): {', '.join(missing)}")
        client = WorkspaceClient(host=host, token=token)
    except Exception as e:
        init_error = f"{type(e).__name__}: {e}"

    # TC1: Catalog Existence (4 points)
    tc1_name = f"TC1: Catalog Existence ({expected_catalog_name})"
    tc1_status = "[FAILED]"
    tc1_score = 0
    tc1_reason = f"Catalog '{expected_catalog_name}' does not exist."

    found_catalog_name = None
    if client:
        try:
            all_cats = [c.name.lower() for c in client.catalogs.list()]
            for cat_opt in catalog_variations:
                if cat_opt in all_cats:
                    catalog_exists = True
                    found_catalog_name = cat_opt
                    tc1_status = "[PASSED]"
                    tc1_score = 4
                    tc1_reason = f"Catalog '{found_catalog_name}' found successfully."
                    break
            if not catalog_exists:
                tc1_reason = f"None of the catalog variations {catalog_variations} exist in Databricks."
        except Exception as e:
            tc1_reason = f"Failed to verify catalog existence: {e}"
    else:
        tc1_reason = f"Failed to initialize Databricks client: {init_error}"

    # TC2: Schema Existence (4 points)
    tc2_name = "TC2: Schema Existence (data)"
    tc2_status = "[FAILED]"
    tc2_score = 0
    tc2_reason = "Prerequisite failed (Catalog does not exist)."

    if catalog_exists:
        try:
            schemas = [s.name.lower() for s in client.schemas.list(catalog_name=found_catalog_name)]
            if 'data' in schemas:
                schema_exists = True
                tc2_status = "[PASSED]"
                tc2_score = 4
                tc2_reason = f"Schema 'data' exists inside catalog '{found_catalog_name}'."
            else:
                tc2_reason = f"Schema 'data' was not found inside catalog '{found_catalog_name}'."
        except Exception as e:
            tc2_reason = f"Failed to verify schema existence: {e}"

    # TC3: Table Ingestion Check (4 points)
    tc3_name = "TC3: Table Ingestion Check (at least one table exists)"
    tc3_status = "[FAILED]"
    tc3_score = 0
    tc3_reason = "Prerequisite failed (Schema 'data' does not exist)."

    target_table = None
    if schema_exists:
        try:
            tables = list(client.tables.list(catalog_name=found_catalog_name, schema_name='data'))
            if tables:
                target_table = tables[0]
                table_exists = True
                tc3_status = "[PASSED]"
                tc3_score = 4
                tc3_reason = f"Found table '{target_table.name}' inside schema '{found_catalog_name}.data'."
            else:
                tc3_reason = f"No tables found inside schema '{found_catalog_name}.data'."
        except Exception as e:
            tc3_reason = f"Failed to list tables in schema: {e}"

    # TC4: Table Structure Verification (4 points)
    tc4_name = "TC4: Table Structure Verification"
    tc4_status = "[FAILED]"
    tc4_score = 0
    tc4_reason = "Prerequisite failed (Table does not exist)."

    if table_exists and target_table:
        try:
            table_info = client.tables.get(full_name=target_table.full_name)
            if table_info.columns and len(table_info.columns) > 0:
                structure_valid = True
                tc4_status = "[PASSED]"
                tc4_score = 4
                cols_str = ", ".join([col.name for col in table_info.columns[:5]])
                if len(table_info.columns) > 5:
                    cols_str += "..."
                tc4_reason = f"Table columns metadata verified: [{cols_str}]."
            else:
                tc4_reason = "Table columns metadata is empty."
        except Exception as e:
            tc4_reason = f"Failed to get table structure metadata: {e}"

    # TC5: Table Format Validation (4 points)
    tc5_name = "TC5: Table Format Validation"
    tc5_status = "[FAILED]"
    tc5_score = 0
    tc5_reason = "Prerequisite failed (Table structure is invalid)."

    if table_exists and target_table:
        try:
            table_info = client.tables.get(full_name=target_table.full_name)
            fmt = str(table_info.data_source_format).upper()
            if "DELTA" in fmt or "CSV" in fmt or "PARQUET" in fmt or "ORC" in fmt:
                format_valid = True
                tc5_status = "[PASSED]"
                tc5_score = 4
                tc5_reason = f"Table format '{fmt}' is verified as valid structured format."
            else:
                tc5_reason = f"Table data format is '{fmt}', expected DELTA or similar."
        except Exception as e:
            tc5_reason = f"Failed to verify table format: {e}"

    # Construct results dict
    results = {
        "tc1": tc1_score == 4,
        "tc2": tc2_score == 4,
        "tc3": tc3_score == 4,
        "tc4": tc4_score == 4,
        "tc5": tc5_score == 4
    }

    try:
        sol_data = {}
        if os.path.exists(sol_path):
            try:
                with open(sol_path, 'r') as f:
                    sol_data = json.load(f)
            except Exception:
                pass
        sol_data['results'] = results
        sol_data['score'] = tc1_score + tc2_score + tc3_score + tc4_score + tc5_score
        with open(sol_path, 'w') as f:
            json.dump(sol_data, f, indent=2)
    except Exception:
        pass

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(results))
    else:
        print_separator()
        print("                KODEBUCK REAL-TIME DATABRICKS AUDIT")
        print_separator()
        print_test_case(tc1_name, tc1_status, tc1_score, 4, tc1_reason)
        print_test_case(tc2_name, tc2_status, tc2_score, 4, tc2_reason)
        print_test_case(tc3_name, tc3_status, tc3_score, 4, tc3_reason)
        print_test_case(tc4_name, tc4_status, tc4_score, 4, tc4_reason)
        print_test_case(tc5_name, tc5_status, tc5_score, 4, tc5_reason)
        
        total_score = tc1_score + tc2_score + tc3_score + tc4_score + tc5_score
        print_separator()
        score_string = f"{total_score}/{max_score}"
        print(f"TOTAL SCORE:{score_string:>57}")
        print_separator()

if __name__ == "__main__":
    verify_task()
