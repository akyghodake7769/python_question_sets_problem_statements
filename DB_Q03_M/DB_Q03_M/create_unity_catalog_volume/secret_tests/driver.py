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
    volume_exists = False
    volume_type_valid = False
    csv_file_present = False
    
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
    # TC3: Volume Existence (4 points)
    # ==========================================
    tc3_name = "TC3: Volume Existence (v1)"
    tc3_status = "[FAILED]"
    tc3_score = 0
    tc3_reason = "Prerequisite failed (Schema 'data' does not exist)."

    actual_volume = None
    if schema_exists:
        try:
            for v in client.volumes.list(catalog_name=catalog_name, schema_name='data'):
                if v.name.lower() == 'v1':
                    volume_exists = True
                    actual_volume = v
                    tc3_status = "[PASSED]"
                    tc3_score = 4
                    tc3_reason = f"Volume 'v1' exists inside '{catalog_name}.data'."
                    break
            if not volume_exists:
                tc3_reason = f"Volume 'v1' was not found inside '{catalog_name}.data'."
        except Exception as e:
            tc3_reason = f"Failed to verify volume existence: {e}"

    # ==========================================
    # TC4: Volume Type Verification (4 points)
    # ==========================================
    tc4_name = "TC4: Volume Type Verification"
    tc4_status = "[FAILED]"
    tc4_score = 0
    tc4_reason = "Prerequisite failed (Volume 'v1' does not exist)."

    if volume_exists and actual_volume:
        try:
            v_type = str(actual_volume.volume_type).upper()
            if "MANAGED" in v_type or "EXTERNAL" in v_type:
                volume_type_valid = True
                tc4_status = "[PASSED]"
                tc4_score = 4
                tc4_reason = f"Volume 'v1' type is verified as {v_type}."
            else:
                tc4_reason = f"Volume type is '{v_type}', expected 'MANAGED' or 'EXTERNAL'."
        except Exception as e:
            tc4_reason = f"Failed to verify volume type: {e}"

    # ==========================================
    # TC5: CSV File Presence (4 points)
    # ==========================================
    tc5_name = "TC5: CSV File Presence in Volume v1"
    tc5_status = "[FAILED]"
    tc5_score = 0
    tc5_reason = "Prerequisite failed (Volume 'v1' does not exist)."

    if volume_exists:
        try:
            # Check directory contents in UC volume path
            volume_path = f"/Volumes/{catalog_name}/data/v1"
            contents = list(client.files.list_directory_contents(directory_path=volume_path))
            csv_files = [f for f in contents if f.path.endswith('.csv')]
            if csv_files:
                csv_file_present = True
                tc5_status = "[PASSED]"
                tc5_score = 4
                tc5_reason = f"Found CSV file(s) in volume: {[os.path.basename(f.path) for f in csv_files]}"
            else:
                tc5_reason = f"No CSV files found inside the volume path: {volume_path}"
        except Exception as e:
            tc5_reason = f"Failed to verify files in volume: {e}"

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
