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

    raw_username = os.getenv("LABSKRAFT_USERNAME") or os.getenv("username") or os.getenv("USER") or "student"
    if '@' in raw_username:
        raw_username = raw_username.split('@')[0]
    if '_' in raw_username:
        raw_username = raw_username.split('_')[0]
    username = raw_username.lower().replace('.', '-')
    
    exam_code = (
        os.getenv("KODEBUCK_EXAM_CODE") or 
        os.getenv("EXAM_CODE") or 
        os.getenv("KODEARENA_EXAM_CODE") or 
        os.getenv("exam_code") or 
        "exam123"
    ).lower()
    
    prefix = f"{username}-{exam_code}"
    catalog_name = f"ut_ltm_{prefix}".lower().replace('-', '_')

    total_score = 0
    max_score = 20
    
    catalog_exists = False
    schema_exists = False
    table_exists = False
    structure_valid = False
    format_valid = False
    
    client = None
    init_error = None
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

    # ==========================================
    # TC1: Catalog Existence (4 points)
    # ==========================================
    tc1_name = f"TC1: Catalog Existence ({catalog_name})"
    tc1_status = "[FAILED]"
    tc1_score = 0
    tc1_reason = f"Catalog '{catalog_name}' does not exist."

    if client:
        try:
            for c in client.catalogs.list():
                if c.name.lower() == catalog_name:
                    catalog_exists = True
                    tc1_status = "[PASSED]"
                    tc1_score = 4
                    tc1_reason = f"Catalog '{catalog_name}' found successfully."
                    break
        except Exception as e:
            tc1_reason = f"Failed to verify catalog existence: {e}"
    else:
        tc1_reason = f"Failed to initialize Databricks client: {init_error}"

    # ==========================================
    # TC2: Schema Existence (4 points)
    # ==========================================
    tc2_name = "TC2: Schema Existence (data)"
    tc2_status = "[FAILED]"
    tc2_score = 0
    tc2_reason = "Prerequisite failed (Catalog does not exist)."

    if catalog_exists:
        try:
            for s in client.schemas.list(catalog_name=catalog_name):
                if s.name.lower() == 'data':
                    schema_exists = True
                    tc2_status = "[PASSED]"
                    tc2_score = 4
                    tc2_reason = f"Schema 'data' exists inside catalog '{catalog_name}'."
                    break
            if not schema_exists:
                tc2_reason = f"Schema 'data' was not found inside catalog '{catalog_name}'."
        except Exception as e:
            tc2_reason = f"Failed to verify schema existence: {e}"

    # ==========================================
    # TC3: Table Ingestion Check (4 points)
    # ==========================================
    tc3_name = "TC3: Table Ingestion Check"
    tc3_status = "[FAILED]"
    tc3_score = 0
    tc3_reason = "Prerequisite failed (Schema 'data' does not exist)."

    target_table = None
    if schema_exists:
        try:
            tables = list(client.tables.list(catalog_name=catalog_name, schema_name='data'))
            if len(tables) > 0:
                table_exists = True
                target_table = tables[0]
                tc3_status = "[PASSED]"
                tc3_score = 4
                tc3_reason = f"Found table '{target_table.name}' inside schema '{catalog_name}.data'."
            else:
                tc3_reason = f"No tables found inside schema '{catalog_name}.data'."
        except Exception as e:
            tc3_reason = f"Failed to list tables in schema: {e}"

    # ==========================================
    # TC4: Table Structure Verification (4 points)
    # ==========================================
    tc4_name = "TC4: Table Structure Verification"
    tc4_status = "[FAILED]"
    tc4_score = 0
    tc4_reason = "Prerequisite failed (Table does not exist)."

    if table_exists and target_table:
        try:
            # Refresh details from API
            t_details = client.tables.get(full_name=target_table.full_name)
            if t_details and t_details.columns and len(t_details.columns) > 0:
                structure_valid = True
                tc4_status = "[PASSED]"
                tc4_score = 4
                cols_str = ", ".join([col.name for col in t_details.columns[:5]])
                if len(t_details.columns) > 5:
                    cols_str += "..."
                tc4_reason = f"Table columns metadata verified: [{cols_str}]."
            else:
                tc4_reason = "Table columns metadata is empty or undefined."
        except Exception as e:
            tc4_reason = f"Failed to retrieve table metadata: {e}"

    # ==========================================
    # TC5: Table Format Validation (4 points)
    # ==========================================
    tc5_name = "TC5: Table Format Validation"
    tc5_status = "[FAILED]"
    tc5_score = 0
    tc5_reason = "Prerequisite failed (Table structure is invalid)."

    if table_exists and target_table:
        try:
            t_details = client.tables.get(full_name=target_table.full_name)
            fmt = str(t_details.data_source_format).upper()
            if "DELTA" in fmt or "CSV" in fmt or "PARQUET" in fmt or "ORC" in fmt:
                format_valid = True
                tc5_status = "[PASSED]"
                tc5_score = 4
                tc5_reason = f"Table format '{fmt}' is verified as valid structured format."
            else:
                tc5_reason = f"Table data format is '{fmt}', expected DELTA or similar."
        except Exception as e:
            tc5_reason = f"Failed to verify table format: {e}"

    # Construct results
    results = {
        "tc1": tc1_score == 4,
        "tc2": tc2_score == 4,
        "tc3": tc3_score == 4,
        "tc4": tc4_score == 4,
        "tc5": tc5_score == 4
    }

    try:
        sol_path = os.path.join(get_base_path(), 'solution.json')
        with open(sol_path, 'w') as f:
            json.dump({'results': results}, f)
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
