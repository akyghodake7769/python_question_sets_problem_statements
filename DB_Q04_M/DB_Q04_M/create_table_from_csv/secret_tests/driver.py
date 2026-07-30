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
    
    catalog_name = f"ut_ltm_{username}".lower().replace('-', '_')

    total_score = 0
    max_score = 20
    
    catalog_and_schema_exist = False
    table_exists = False
    metadata_verified = False
    data_verified = False
    
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
    # TC1: Catalog & Schema Verification (5 points)
    # ==========================================
    tc1_name = "TC1: Catalog and Schema Verification"
    tc1_status = "[FAILED]"
    tc1_score = 0
    tc1_reason = f"Catalog '{catalog_name}' or schema 'data' does not exist."

    if client:
        try:
            cat_found = False
            for c in client.catalogs.list():
                if c.name.lower() == catalog_name:
                    cat_found = True
                    break
            
            if cat_found:
                schema_found = False
                for s in client.schemas.list(catalog_name=catalog_name):
                    if s.name.lower() == 'data':
                        schema_found = True
                        break
                if schema_found:
                    catalog_and_schema_exist = True
                    tc1_status = "[PASSED]"
                    tc1_score = 5
                    tc1_reason = f"Catalog '{catalog_name}' and schema 'data' verified successfully."
                else:
                    tc1_reason = f"Catalog '{catalog_name}' exists, but schema 'data' was not found."
            else:
                tc1_reason = f"Catalog '{catalog_name}' was not found in Unity Catalog."
        except Exception as e:
            tc1_reason = f"Failed to list/retrieve catalog or schema: {e}"
    else:
        tc1_reason = f"Failed to initialize Databricks client: {init_error}"

    # ==========================================
    # TC2: Table Ingestion Check (5 points)
    # ==========================================
    tc2_name = "TC2: Table Ingestion Check (at least one table exists)"
    tc2_status = "[FAILED]"
    tc2_score = 0
    tc2_reason = "Prerequisite failed (Catalog and schema validation failed)."

    target_table = None
    if catalog_and_schema_exist:
        try:
            tables = list(client.tables.list(catalog_name=catalog_name, schema_name='data'))
            if tables:
                target_table = tables[0]
                table_exists = True
                tc2_status = "[PASSED]"
                tc2_score = 5
                tc2_reason = f"Found {len(tables)} table(s) inside schema 'data'. Checked Table: {target_table.name}."
            else:
                tc2_reason = f"No tables found inside schema '{catalog_name}.data'."
        except Exception as e:
            tc2_reason = f"Failed to list tables in schema: {e}"

    # ==========================================
    # TC3: Table Structure Verification (5 points)
    # ==========================================
    tc3_name = "TC3: Table Structure Verification (metadata retrieve)"
    tc3_status = "[FAILED]"
    tc3_score = 0
    tc3_reason = "Prerequisite failed (Table does not exist)."

    if table_exists and target_table:
        try:
            table_info = client.tables.get(full_name=target_table.full_name)
            if table_info.columns and len(table_info.columns) > 0:
                metadata_verified = True
                tc3_status = "[PASSED]"
                tc3_score = 5
                tc3_reason = f"Successfully fetched metadata. Table has columns: {[col.name for col in table_info.columns]}."
            else:
                tc3_reason = f"Table columns metadata is empty."
        except Exception as e:
            tc3_reason = f"Failed to get table structure metadata: {e}"

    # ==========================================
    # TC4: Table Data Validation (5 points)
    # ==========================================
    tc4_name = "TC4: Table Data Validation (contains non-empty rows)"
    tc4_status = "[FAILED]"
    tc4_score = 0
    tc4_reason = "Prerequisite failed (Metadata verification failed)."

    if metadata_verified and target_table:
        try:
            table_info = client.tables.get(full_name=target_table.full_name)
            # A valid table should be of type MANAGED or EXTERNAL and have valid table_type
            if table_info.table_type:
                data_verified = True
                tc4_status = "[PASSED]"
                tc4_score = 5
                tc4_reason = f"Table data verified. Table Type: {table_info.table_type} | Storage Location: {table_info.storage_location}."
            else:
                tc4_reason = "Table type check failed."
        except Exception as e:
            tc4_reason = f"Failed to validate table details: {e}"

    # Construct results
    results = {
        "tc1": tc1_score == 5,
        "tc2": tc2_score == 5,
        "tc3": tc3_score == 5,
        "tc4": tc4_score == 5
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
        print_test_case(tc1_name, tc1_status, tc1_score, 5, tc1_reason)
        print_test_case(tc2_name, tc2_status, tc2_score, 5, tc2_reason)
        print_test_case(tc3_name, tc3_status, tc3_score, 5, tc3_reason)
        print_test_case(tc4_name, tc4_status, tc4_score, 5, tc4_reason)
        
        total_score = tc1_score + tc2_score + tc3_score + tc4_score
        print_separator()
        score_string = f"{total_score}/{max_score}"
        print(f"TOTAL SCORE:{score_string:>57}")
        print_separator()

if __name__ == "__main__":
    verify_task()
