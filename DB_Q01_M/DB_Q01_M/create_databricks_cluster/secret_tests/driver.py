import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def print_separator():
    print("-" * 70)

def print_test_case(name, status, score, max_score, reason):
    # Dynamically calculate the number of dots to align the right side perfectly
    pad_length = 63 - len(name) - 1
    if pad_length < 1: 
        pad_length = 1
    dots = "." * pad_length
    print(f"{name} {dots} {status} ({score}/{max_score})")
    print(f"    └─ [Reason]: {reason}")

def verify_task():
    # Configure stdout to handle UTF-8 if we are on Windows
    if sys.platform.startswith('win'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    # 1. Resolve student info
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
    
    target_cluster_name = f"{username}-{exam_code}-db-cluster"

    total_score = 0
    max_score = 20
    
    # Track states for prerequisites
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

    # ==========================================
    # TC1: Cluster Existence (4 points)
    # ==========================================
    tc1_name = "TC1: Cluster Existence"
    tc1_status = "[FAILED]"
    tc1_score = 0
    tc1_reason = f"Cluster '{target_cluster_name}' does not exist."

    if client:
        try:
            # List clusters and find the target cluster
            for c in client.clusters.list():
                if c.cluster_name == target_cluster_name:
                    cluster = c
                    cluster_exists = True
                    break
            
            if cluster_exists:
                tc1_status = "[PASSED]"
                tc1_score = 4
                tc1_reason = "Cluster was found successfully."
            else:
                tc1_reason = f"Cluster '{target_cluster_name}' was not found in the workspace."
        except Exception as e:
            tc1_reason = f"Failed to list/retrieve cluster information: {e}"
    else:
        tc1_reason = f"Failed to initialize Databricks client. Reason: {init_error}"

    # ==========================================
    # TC2: Spark Runtime Version (17.3 LTS) (4 points)
    # ==========================================
    tc2_name = "TC2: Spark Runtime Version (17.3 LTS)"
    tc2_status = "[FAILED]"
    tc2_score = 0
    tc2_reason = "Prerequisite failed (Cluster invalid or not found)."

    if cluster_exists and cluster:
        try:
            runtime = cluster.spark_version
            # 17.3 LTS runtime string is 17.3.x-scala2.13.
            if runtime and ("17.3" in runtime) and ("scala2.13" in runtime):
                tc2_status = "[PASSED]"
                tc2_score = 4
                tc2_reason = f"Spark runtime is correct ({runtime})."
            else:
                tc2_reason = f"Runtime is '{runtime}', expected '17.3.x-scala2.13'."
        except Exception as e:
            tc2_reason = f"Could not verify Spark runtime version: {e}"

    # ==========================================
    # TC3: Autotermination Verification (4 points)
    # ==========================================
    tc3_name = "TC3: Autotermination (30 minutes)"
    tc3_status = "[FAILED]"
    tc3_score = 0
    tc3_reason = "Prerequisite failed."

    if cluster_exists and cluster:
        try:
            auto_term = cluster.autotermination_minutes
            if auto_term == 30:
                tc3_status = "[PASSED]"
                tc3_score = 4
                tc3_reason = "Autotermination is set to 30 minutes."
            else:
                tc3_reason = f"Autotermination is set to {auto_term} minutes, expected 30."
        except Exception as e:
            tc3_reason = f"Could not verify autotermination: {e}"

    # ==========================================
    # TC4: Single Node Mode Enabled (4 points)
    # ==========================================
    tc4_name = "TC4: Single Node Mode Enabled"
    tc4_status = "[FAILED]"
    tc4_score = 0
    tc4_reason = "Prerequisite failed."

    if cluster_exists and cluster:
        try:
            num_workers = cluster.num_workers
            spark_conf = cluster.spark_conf or {}
            profile = spark_conf.get("spark.databricks.cluster.profile")
            
            is_single_node = (num_workers == 0 or num_workers is None) and (profile == "singleNode")
            
            if is_single_node:
                tc4_status = "[PASSED]"
                tc4_score = 4
                tc4_reason = "Single Node mode is enabled (0 workers and singleNode profile)."
            else:
                reason_parts = []
                if num_workers != 0:
                    reason_parts.append(f"num_workers={num_workers}")
                if profile != "singleNode":
                    reason_parts.append(f"profile='{profile}'")
                tc4_reason = f"Cluster is not configured for Single Node (found: {', '.join(reason_parts)})."
        except Exception as e:
            tc4_reason = f"Could not verify single node mode: {e}"

    # ==========================================
    # TC5: Node Type Standard_F4 & Photon Disabled (4 points)
    # ==========================================
    tc5_name = "TC5: Node Type Standard_F4 & Photon Disabled"
    tc5_status = "[FAILED]"
    tc5_score = 0
    tc5_reason = "Prerequisite failed."

    if cluster_exists and cluster:
        try:
            node_type = cluster.node_type_id
            runtime = cluster.spark_version or ""
            
            # Check Photon: Photon runtime has "-photon-" in the spark_version (e.g. 17.3.x-photon-scala2.12)
            photon_disabled = "-photon" not in runtime.lower()
            node_type_ok = (node_type == "Standard_F4")
            
            if node_type_ok and photon_disabled:
                tc5_status = "[PASSED]"
                tc5_score = 4
                tc5_reason = "Node Type is Standard_F4 and Photon Acceleration is disabled."
            else:
                reasons = []
                if not node_type_ok:
                    reasons.append(f"Node Type is '{node_type}', expected 'Standard_F4'")
                if not photon_disabled:
                    reasons.append("Photon Acceleration is enabled")
                tc5_reason = " / ".join(reasons)
        except Exception as e:
            tc5_reason = f"Could not verify node type and photon settings: {e}"

    # Construct results dict
    results = {
        "tc1": tc1_score == 4,
        "tc2": tc2_score == 4,
        "tc3": tc3_score == 4,
        "tc4": tc4_score == 4,
        "tc5": tc5_score == 4
    }

    # Write solution.json file locally
    try:
        sol_path = os.path.join(get_base_path(), 'solution.json')
        with open(sol_path, 'w') as f:
            json.dump({'results': results}, f)
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

if __name__ == "__main__":
    verify_task()
