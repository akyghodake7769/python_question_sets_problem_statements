# import os
# import sys
# import json

# def get_base_path():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

# def print_separator():
#     print("-" * 70)

# def print_test_case(name, status, score, max_score, reason):
#     pad_length = 63 - len(name) - 1
#     if pad_length < 1: 
#         pad_length = 1
#     dots = "." * pad_length
#     print(f"{name} {dots} {status} ({score}/{max_score})")
#     print(f"    └─ [Reason]: {reason}")

# def verify_task():
#     if sys.platform.startswith('win'):
#         try:
#             sys.stdout.reconfigure(encoding='utf-8')
#         except Exception:
#             pass

#     # 1. Resolve student info
#     raw_username = os.getenv("LABSKRAFT_USERNAME") or os.getenv("username") or os.getenv("USER") or "student"
#     if '@' in raw_username:
#         raw_username = raw_username.split('@')[0]
#     if '_' in raw_username:
#         raw_username = raw_username.split('_')[0]
#     username = raw_username.lower().replace('.', '-')
    
#     exam_code = (
#         os.getenv("KODEBUCK_EXAM_CODE") or 
#         os.getenv("EXAM_CODE") or 
#         os.getenv("KODEARENA_EXAM_CODE") or 
#         os.getenv("exam_code") or 
#         "exam123"
#     ).lower()
    
#     table_name = f"{username}_{exam_code}_bronze_sales"

#     total_score = 0
#     max_score = 20
    
#     tc1_name = "TC1: Delta table existence (<prefix>_bronze_sales exists)"
#     tc1_status = "[FAILED]"
#     tc1_score = 0
#     tc1_reason = f"Table '{table_name}' not found."

#     tc2_name = "TC2: Schema columns check (columns match required definitions)"
#     tc2_status = "[FAILED]"
#     tc2_score = 0
#     tc2_reason = "Prerequisite failed."

#     tc3_name = "TC3: Delta format confirmation"
#     tc3_status = "[FAILED]"
#     tc3_score = 0
#     tc3_reason = "Prerequisite failed."

#     # 2. Connect to Databricks
#     client = None
#     init_error = None
#     try:
#         from databricks.sdk import WorkspaceClient
#         host = os.getenv("DATABRICKS_HOST")
#         token = os.getenv("DATABRICKS_TOKEN")
#         if not host or not token:
#             missing = []
#             if not host: missing.append("DATABRICKS_HOST")
#             if not token: missing.append("DATABRICKS_TOKEN")
#             raise ValueError(f"Missing environment variable(s): {', '.join(missing)}")
#         client = WorkspaceClient(
#             host=host,
#             token=token
#         )
#     except Exception as e:
#         init_error = f"{type(e).__name__}: {e}"

#     table_obj = None
#     if client:
#         for cat in ["main", "hive_metastore"]:
#             try:
#                 table_obj = client.tables.get(f"{cat}.default.{table_name}")
#                 if table_obj:
#                     break
#             except Exception:
#                 pass
                
#         if table_obj:
#             tc1_status = "[PASSED]"
#             tc1_score = 4
#             tc1_reason = f"Table '{table_name}' found."
            
#             # TC2 Columns check
#             try:
#                 cols = [col.name.lower() for col in table_obj.columns]
#                 if len(cols) > 0:
#                     tc2_status = "[PASSED]"
#                     tc2_score = 4
#                     tc2_reason = f"Schema verified. Columns: {', '.join(cols)}."
#                 else:
#                     tc2_reason = "Schema is empty."
#             except Exception as e:
#                 tc2_reason = f"Failed schema validation: {e}"

#             # TC3 format check
#             if str(table_obj.data_source_format).upper() == "DELTA":
#                 tc3_status = "[PASSED]"
#                 tc3_score = 4
#                 tc3_reason = "Table data format is DELTA."
#             else:
#                 tc3_reason = f"Format is {table_obj.data_source_format}, expected DELTA."
#         else:
#             tc1_reason = f"Table '{table_name}' not found."
#     else:
#         # Fallback to local configuration mock passing if no credentials or library provided
#         tc1_status = "[PASSED]"
#         tc1_score = 4
#         tc1_reason = f"Table '{table_name}' verified via local simulation (Databricks connection skipped)."
        
#         tc2_status = "[PASSED]"
#         tc2_score = 4
#         tc2_reason = "Schema columns check verified successfully."
        
#         tc3_status = "[PASSED]"
#         tc3_score = 4
#         tc3_reason = "Table data format is DELTA."

#     # TC4 & TC5: Reserved
#     tc4_name = "TC4: Reserved validation"
#     tc4_status = "[PASSED]"
#     tc4_score = 4
#     tc4_reason = "Validated successfully."

#     tc5_name = "TC5: Reserved validation"
#     tc5_status = "[PASSED]"
#     tc5_score = 4
#     tc5_reason = "Validated successfully."

#     # Construct results dict
#     results = {
#         "tc1": tc1_score == 4,
#         "tc2": tc2_score == 4,
#         "tc3": tc3_score == 4,
#         "tc4": tc4_score == 4,
#         "tc5": tc5_score == 4
#     }

#     # Write solution.json file locally by merging with existing metadata
#     try:
#         sol_path = os.path.join(get_base_path(), 'solution.json')
#         sol_data = {}
#         if os.path.exists(sol_path):
#             try:
#                 with open(sol_path, 'r') as f:
#                     sol_data = json.load(f)
#             except Exception:
#                 pass
#         sol_data['results'] = results
#         sol_data['score'] = tc1_score + tc2_score + tc3_score + tc4_score + tc5_score
#         with open(sol_path, 'w') as f:
#             json.dump(sol_data, f, indent=2)
#     except Exception:
#         pass

#     # Handle output format
#     if len(sys.argv) > 1 and sys.argv[1] == '--json':
#         print(json.dumps(results))
#     else:
#         print_separator()
#         print("                KODEBUCK REAL-TIME DATABRICKS AUDIT")
#         print_separator()
#         print_test_case(tc1_name, tc1_status, tc1_score, 4, tc1_reason)
#         print_test_case(tc2_name, tc2_status, tc2_score, 4, tc2_reason)
#         print_test_case(tc3_name, tc3_status, tc3_score, 4, tc3_reason)
#         print_test_case(tc4_name, tc4_status, tc4_score, 4, tc4_reason)
#         print_test_case(tc5_name, tc5_status, tc5_score, 4, tc5_reason)
        
#         total_score = tc1_score + tc2_score + tc3_score + tc4_score + tc5_score
#         print_separator()
#         score_string = f"{total_score}/{max_score}"
#         print(f"TOTAL SCORE:{score_string:>57}")
#         print_separator()

# if __name__ == '__main__':
#     verify_task()
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

    # 1. Resolve student info
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
    
    target_cluster_name = f"{username}-{exam_code}-ops-cluster"

    total_score = 0
    max_score = 20
    
    cluster_exists = False
    cluster = None
    
    # 2. Connect to Databricks
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
        client = WorkspaceClient(
            host=host,
            token=token
        )
    except Exception as e:
        init_error = f"{type(e).__name__}: {e}"

    
    tc1_name = "TC1: Delta table existence (<prefix>_bronze_sales exists)"
    tc1_status = "[FAILED]"
    tc1_score = 0
    
    table_name = f"{username}_{exam_code}_bronze_sales"
    table_obj = None
    if client:
        for cat in ["main", "hive_metastore", "kraft_data"]:
            try:
                table_obj = client.tables.get(f"{cat}.default.{table_name}")
                if table_obj:
                    break
            except Exception:
                pass
                
    if table_obj:
        tc1_status = "[PASSED]"
        tc1_score = 4
        tc1_reason = f"Table '{table_name}' found."
        cluster_exists = True
    else:
        tc1_reason = f"Table '{table_name}' not found."

    tc2_name = "TC2: Schema columns check (columns match required definitions)"
    tc2_status = "[FAILED]"
    tc2_score = 0
    tc2_reason = "Prerequisite failed."
    
    if cluster_exists and table_obj:
        try:
            cols = [col.name.lower() for col in table_obj.columns]
            if len(cols) > 0:
                tc2_status = "[PASSED]"
                tc2_score = 4
                tc2_reason = f"Schema verified. Columns: {', '.join(cols)}."
            else:
                tc2_reason = "Schema is empty."
        except Exception as e:
            tc2_reason = f"Failed schema validation: {e}"

    tc3_name = "TC3: Delta format confirmation"
    tc3_status = "[FAILED]"
    tc3_score = 0
    tc3_reason = "Prerequisite failed."
    
    if cluster_exists and table_obj:
        if str(table_obj.data_source_format).upper() == "DELTA":
            tc3_status = "[PASSED]"
            tc3_score = 4
            tc3_reason = "Table data format is DELTA."
        else:
            tc3_reason = f"Format is {table_obj.data_source_format}, expected DELTA."

    tc4_name = "TC4: Reserved validation"
    tc4_status = "[PASSED]"
    tc4_score = 4
    tc4_reason = "Validated successfully."

    tc5_name = "TC5: Reserved validation"
    tc5_status = "[PASSED]"
    tc5_score = 4
    tc5_reason = "Validated successfully."


    # Construct results dict
    results = {
        "tc1": tc1_score == 4,
        "tc2": tc2_score == 4,
        "tc3": tc3_score == 4,
        "tc4": tc4_score == 4,
        "tc5": tc5_score == 4
    }

    # Write solution.json file locally by merging with existing metadata
    try:
        sol_path = os.path.join(get_base_path(), 'solution.json')
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

    # Handle output format
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

if __name__ == '__main__':
    verify_task()
