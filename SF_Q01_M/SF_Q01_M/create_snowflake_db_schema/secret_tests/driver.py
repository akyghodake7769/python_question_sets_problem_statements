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

    labskraft_username = os.getenv("LABSKRAFT_USERNAME") or "student"
    exam_code = os.getenv("KODEBUCK_EXAM_CODE") or os.getenv("EXAM_CODE") or "UNKNOWN"
    
    sol_path = os.path.join(get_base_path(), 'solution.json')
    if os.path.exists(sol_path):
        try:
            with open(sol_path, 'r') as f:
                data = json.load(f)
            if data.get('labskraft_username'):
                labskraft_username = data['labskraft_username']
            if data.get('exam_code'):
                exam_code = data['exam_code']
        except Exception:
            pass

    raw_username = labskraft_username
    if '@' in raw_username:
        raw_username = raw_username.split('@')[0]
    if '_' in raw_username:
        raw_username = raw_username.split('_')[0]
    username = raw_username.lower().replace('.', '-')
    
    if exam_code and exam_code != "UNKNOWN":
        prefix = f"{username}_{exam_code.lower()}"
    else:
        prefix = username
        
    db_name = f"sn_ltm_{prefix}".upper().replace('-', '_')

    total_score = 0
    max_score = 20
    
    db_exists = False
    schema_exists = False
    table_exists = False
    query_success = False
    
    conn = None
    init_error = None
    
    # 1. Connect to Snowflake
    try:
        import snowflake.connector
        user = os.getenv("SNOWFLAKE_USER") or "LTM_DEMO"
        password = os.getenv("SNOWFLAKE_PASSWORD") or "KloudKraft@2026"
        account = os.getenv("SNOWFLAKE_ACCOUNT") or "WJB07325.ap-south-1.aws"
        warehouse = os.getenv("SNOWFLAKE_WAREHOUSE") or "COMPUTE_WH"
        
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse
        )
    except Exception as e:
        init_error = f"{type(e).__name__}: {e}"

    # ==========================================
    # TC1: Database Existence (5 points)
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
                tc1_score = 5
                tc1_reason = f"Database '{db_name}' found successfully."
            else:
                tc1_reason = f"Database '{db_name}' was not found in Snowflake."
        except Exception as e:
            tc1_reason = f"Failed to verify database existence: {e}"
    else:
        tc1_reason = f"Failed to initialize Snowflake connection: {init_error}"

    # ==========================================
    # TC2: Schema Existence (5 points)
    # ==========================================
    tc2_name = "TC2: Schema Existence (DATA)"
    tc2_status = "[FAILED]"
    tc2_score = 0
    tc2_reason = "Prerequisite failed (Database does not exist)."

    if db_exists:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SHOW SCHEMAS IN DATABASE {db_name}")
            results = cursor.fetchall()
            # In SHOW SCHEMAS, the schema name is in the 2nd column (index 1)
            if any(row[1].upper() == 'DATA' for row in results):
                schema_exists = True
                tc2_status = "[PASSED]"
                tc2_score = 5
                tc2_reason = f"Schema 'DATA' exists inside database '{db_name}'."
            else:
                tc2_reason = f"Schema 'DATA' was not found inside database '{db_name}'."
        except Exception as e:
            tc2_reason = f"Failed to verify schema existence: {e}"


    # ==========================================
    # TC3: Table and Data Load (5 points)
    # ==========================================
    tc3_name = "TC3: Table and Data Load (CSV Ingestion Check)"
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
                tc3_score = 5
                tc3_reason = f"Found {len(tables)} table(s) in schema. Target Table: '{target_table_name}'."
            else:
                tc3_reason = f"No tables found inside '{db_name}.DATA'."
        except Exception as e:
            tc3_reason = f"Failed to list tables in schema: {e}"

    # ==========================================
    # TC4: Query Execution Validation (5 points)
    # ==========================================
    tc4_name = "TC4: Query Execution Validation (Worksheet query checks)"
    tc4_status = "[FAILED]"
    tc4_score = 0
    tc4_reason = "Prerequisite failed (Table does not exist)."

    if table_exists and target_table_name:
        try:
            cursor = conn.cursor()
            # Perform query on the ingested table to count records
            cursor.execute(f"SELECT COUNT(*) FROM {db_name}.DATA.{target_table_name}")
            row_count = cursor.fetchone()[0]
            if row_count > 0:
                query_success = True
                tc4_status = "[PASSED]"
                tc4_score = 5
                tc4_reason = f"Query executed successfully on '{target_table_name}'. Ingested row count: {row_count}."
            else:
                tc4_reason = f"Table '{target_table_name}' exists but contains 0 rows."
        except Exception as e:
            tc4_reason = f"Failed to query table: {e}"

    # Close connection
    if conn:
        try:
            conn.close()
        except Exception:
            pass

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
        print("                KODEBUCK REAL-TIME SNOWFLAKE AUDIT")
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
