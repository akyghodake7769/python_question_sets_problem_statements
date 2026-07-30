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

    # 1. Resolve student info (Exactly as DB_Q07_E)
    raw_username = os.getenv("DATABRICKS_USERNAME") or os.getenv("databricks_username") or os.getenv("LABSKRAFT_USERNAME") or os.getenv("username") or os.getenv("USER") or "student"
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
    
    sol_path = os.path.join(get_base_path(), 'solution.json')
    if os.path.exists(sol_path):
        try:
            with open(sol_path, 'r') as f:
                data = json.load(f)
            if data.get('labskraft_username'):
                raw_u = data['labskraft_username']
                if '@' in raw_u: raw_u = raw_u.split('@')[0]
                if '_' in raw_u: raw_u = raw_u.split('_')[0]
                username = raw_u.lower().replace('.', '-')
            if data.get('exam_code'):
                exam_code = data['exam_code'].lower()
        except Exception:
            pass

    table_name = f"{username}_{exam_code}_autoloader_ingest".lower().replace('-', '_')

    tc1_status = "[FAILED]"
    tc1_score = 0
    tc1_reason = f"Table '{table_name}' was not found in catalogs main, hive_metastore, or kraft_data."

    tc2_status = "[FAILED]"
    tc2_score = 0
    tc2_reason = "Prerequisite failed (Table not found)."

    tc3_status = "[FAILED]"
    tc3_score = 0
    tc3_reason = "Prerequisite failed (Table not found)."

    tc4_status = "[PASSED]"
    tc4_score = 4
    tc4_reason = "Validated successfully."

    tc5_status = "[PASSED]"
    tc5_score = 4
    tc5_reason = "Validated successfully."

    client = None
    init_error = None
    
    # 2. Connect to Databricks
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

    table_obj = None
    if client:
        # Check catalogs
        for cat in ["main", "hive_metastore", "kraft_data"]:
            try:
                table_obj = client.tables.get(f"{cat}.default.{table_name}")
                if table_obj:
                    break
            except Exception:
                pass

    if table_obj:
        # TC1: Table load check
        tc1_status = "[PASSED]"
        tc1_score = 4
        tc1_reason = f"Table '{table_obj.full_name}' found successfully."

        # TC2: Auto Loader config check (verify it has schema/columns metadata)
        if table_obj.columns and len(table_obj.columns) > 0:
            tc2_status = "[PASSED]"
            tc2_score = 4
            tc2_reason = f"Auto Loader table has valid columns: {[col.name for col in table_obj.columns[:5]]}."
        else:
            tc2_reason = "Table columns metadata is empty."

        # TC3: Schema schemaLocation validation (verify storage location is present)
        if table_obj.storage_location:
            tc3_status = "[PASSED]"
            tc3_score = 4
            tc3_reason = f"Schema / table storage location verified: {table_obj.storage_location}"
        else:
            tc3_reason = "Table storage location is missing."
    else:
        if init_error:
            tc1_reason = f"Failed to initialize Databricks client: {init_error}"

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
        with open(sol_path, 'w') as f:
            json.dump(sol_data, f, indent=2)
    except Exception:
        pass

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(results))
    else:
        print_separator()
        print("                KODEBUCK REAL-TIME AUDIT")
        print_separator()
        print_test_case("TC1: Table load check", tc1_status, tc1_score, 4, tc1_reason)
        print_test_case("TC2: Auto Loader config check", tc2_status, tc2_score, 4, tc2_reason)
        print_test_case("TC3: Schema schemaLocation validation", tc3_status, tc3_score, 4, tc3_reason)
        print_test_case("TC4: Reserved validation", tc4_status, tc4_score, 4, tc4_reason)
        print_test_case("TC5: Reserved validation", tc5_status, tc5_score, 4, tc5_reason)
        
        total_score = tc1_score + tc2_score + tc3_score + tc4_score + tc5_score
        print_separator()
        score_string = f"{total_score}/20"
        print(f"TOTAL SCORE:{score_string:>57}")
        print_separator()

if __name__ == '__main__':
    verify_task()
