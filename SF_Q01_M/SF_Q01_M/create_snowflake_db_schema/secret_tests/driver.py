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
    db_name = f"sn_ltm_{prefix}".upper().replace('-', '_')

    total_score = 0
    max_score = 20
    
    db_exists = False
    schema_exists = False
    table_exists = False
    columns_valid = False
    query_success = False
    
    conn = None
    init_error = None
    
    # 1. Connect to Snowflake
    try:
        import snowflake.connector
        user = os.getenv("SNOWFLAKE_USER")
        password = os.getenv("SNOWFLAKE_PASSWORD")
        account = os.getenv("SNOWFLAKE_ACCOUNT")
        warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
        
        if not user or not password or not account:
            missing = []
            if not user: missing.append("SNOWFLAKE_USER")
            if not password: missing.append("SNOWFLAKE_PASSWORD")
            if not account: missing.append("SNOWFLAKE_ACCOUNT")
            raise ValueError(f"Missing environment variable(s): {', '.join(missing)}")
            
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse
        )
    except Exception as e:
        init_error = f"{type(e).__name__}: {e}"

    # ==========================================
    # TC1: Database Existence (4 points)
    # ==========================================
    tc1_name = f"TC1: Database Existence ({db_name})"
    tc1_status = "[FAILED]"
    tc1_score = 0
    tc1_reason = f"Database '{db_name}' does not exist."

    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            results = cursor.fetchall()
            if results:
                db_exists = True
                tc1_status = "[PASSED]"
                tc1_score = 4
                tc1_reason = f"Database '{db_name}' found successfully."
            else:
                tc1_reason = f"Database '{db_name}' was not found in Snowflake."
        except Exception as e:
            tc1_reason = f"Failed to verify database existence: {e}"
    else:
        tc1_reason = f"Failed to initialize Snowflake connection: {init_error}"

    # ==========================================
    # TC2: Schema Existence (4 points)
    # ==========================================
    tc2_name = "TC2: Schema Existence (DATA)"
    tc2_status = "[FAILED]"
    tc2_score = 0
    tc2_reason = "Prerequisite failed (Database does not exist)."

    if db_exists:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SHOW SCHEMAS IN DATABASE {db_name} LIKE 'DATA'")
            results = cursor.fetchall()
            if results:
                schema_exists = True
                tc2_status = "[PASSED]"
                tc2_score = 4
                tc2_reason = f"Schema 'DATA' exists inside database '{db_name}'."
            else:
                tc2_reason = f"Schema 'DATA' was not found inside database '{db_name}'."
        except Exception as e:
            tc2_reason = f"Failed to verify schema existence: {e}"

    # ==========================================
    # TC3: Table Ingestion Check (4 points)
    # ==========================================
    tc3_name = "TC3: Table Ingestion Check"
    tc3_status = "[FAILED]"
    tc3_score = 0
    tc3_reason = "Prerequisite failed (Schema 'DATA' does not exist)."

    target_table_name = None
    if schema_exists:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SHOW TABLES IN SCHEMA {db_name}.DATA")
            tables = cursor.fetchall()
            if tables:
                # tables columns in SHOW TABLES format: name is in column index 1
                target_table_name = tables[0][1]
                table_exists = True
                tc3_status = "[PASSED]"
                tc3_score = 4
                tc3_reason = f"Found {len(tables)} table(s) in schema. Target Table: '{target_table_name}'."
            else:
                tc3_reason = f"No tables found inside '{db_name}.DATA'."
        except Exception as e:
            tc3_reason = f"Failed to list tables in schema: {e}"

    # ==========================================
    # TC4: Table Column Verification (4 points)
    # ==========================================
    tc4_name = "TC4: Table Column Verification"
    tc4_status = "[FAILED]"
    tc4_score = 0
    tc4_reason = "Prerequisite failed (Table does not exist)."

    if table_exists and target_table_name:
        try:
            cursor = conn.cursor()
            cursor.execute(f"DESCRIBE TABLE {db_name}.DATA.{target_table_name}")
            cols = cursor.fetchall()
            if cols and len(cols) > 0:
                columns_valid = True
                tc4_status = "[PASSED]"
                tc4_score = 4
                cols_str = ", ".join([row[0] for row in cols[:5]])
                if len(cols) > 5:
                    cols_str += "..."
                tc4_reason = f"Verified columns in '{target_table_name}': [{cols_str}]."
            else:
                tc4_reason = f"No column descriptions found for '{target_table_name}'."
        except Exception as e:
            tc4_reason = f"Failed to describe table columns: {e}"

    # ==========================================
    # TC5: Table Data Verification (4 points)
    # ==========================================
    tc5_name = "TC5: Table Data Verification"
    tc5_status = "[FAILED]"
    tc5_score = 0
    tc5_reason = "Prerequisite failed (Table columns verification failed)."

    if columns_valid and target_table_name:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {db_name}.DATA.{target_table_name}")
            row_count = cursor.fetchone()[0]
            if row_count > 0:
                query_success = True
                tc5_status = "[PASSED]"
                tc5_score = 4
                tc5_reason = f"Table contains data rows. Total row count: {row_count}."
            else:
                tc5_reason = f"Table '{target_table_name}' exists but contains 0 rows."
        except Exception as e:
            tc5_reason = f"Failed to query table data: {e}"

    # Close connection
    if conn:
        try:
            conn.close()
        except Exception:
            pass

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
        print("                KODEBUCK REAL-TIME SNOWFLAKE AUDIT")
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
