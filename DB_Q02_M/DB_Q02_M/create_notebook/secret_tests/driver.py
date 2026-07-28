import os
import sys
import base64

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
    username = os.getenv("LABSKRAFT_USERNAME", "student")
    exam_code = os.getenv("KODEBUCK_EXAM_CODE", "exam123")
    target_dir = f"/Shared/{username}-{exam_code}-workspace"
    target_notebook = f"{target_dir}/data-analysis"

    print_separator()
    print("                KODEBUCK REAL-TIME DATABRICKS AUDIT")
    print_separator()

    total_score = 0
    max_score = 25
    
    # Track states for prerequisites
    dir_exists = False
    notebook_exists = False
    object_is_notebook = False
    language_is_python = False
    
    notebook_status = None

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
    # TC1: Directory Existence (5 points)
    # ==========================================
    tc1_name = "TC1: Directory Existence (/Shared/<prefix>-workspace)"
    tc1_status = "[FAILED]"
    tc1_score = 0
    tc1_reason = f"Directory '{target_dir}' does not exist."

    if client:
        try:
            from databricks.sdk.errors import NotFound
            from databricks.sdk.service.workspace import ObjectType
            
            try:
                dir_status = client.workspace.get_status(path=target_dir)
                if dir_status.object_type == ObjectType.DIRECTORY:
                    tc1_status = "[PASSED]"
                    tc1_score = 5
                    tc1_reason = "Workspace directory exists and is a directory."
                    dir_exists = True
                else:
                    tc1_reason = f"Path '{target_dir}' exists but is of type '{dir_status.object_type}', expected 'DIRECTORY'."
            except NotFound:
                tc1_reason = f"Directory '{target_dir}' was not found in the workspace."
        except Exception as e:
            tc1_reason = f"Failed to list or retrieve workspace status: {e}"
    else:
        tc1_reason = f"Failed to initialize Databricks client. Reason: {init_error}"

    print_test_case(tc1_name, tc1_status, tc1_score, 5, tc1_reason)

    # ==========================================
    # TC2: Notebook Existence (5 points)
    # ==========================================
    tc2_name = "TC2: Notebook Existence (data-analysis)"
    tc2_status = "[FAILED]"
    tc2_score = 0
    tc2_reason = "Prerequisite failed (Directory not found)."

    if dir_exists and client:
        try:
            from databricks.sdk.errors import NotFound
            try:
                notebook_status = client.workspace.get_status(path=target_notebook)
                tc2_status = "[PASSED]"
                tc2_score = 5
                tc2_reason = "Notebook exists successfully."
                notebook_exists = True
            except NotFound:
                tc2_reason = f"Notebook '{target_notebook}' was not found."
        except Exception as e:
            tc2_reason = f"Error checking notebook existence: {e}"

    print_test_case(tc2_name, tc2_status, tc2_score, 5, tc2_reason)

    # ==========================================
    # TC3: Object Type Verification (5 points)
    # ==========================================
    tc3_name = "TC3: Object Type Verification (NOTEBOOK)"
    tc3_status = "[FAILED]"
    tc3_score = 0
    tc3_reason = "Prerequisite failed (Notebook not found)."

    if notebook_exists and notebook_status:
        try:
            from databricks.sdk.service.workspace import ObjectType
            if notebook_status.object_type == ObjectType.NOTEBOOK:
                tc3_status = "[PASSED]"
                tc3_score = 5
                tc3_reason = "Object is confirmed to be a NOTEBOOK."
                object_is_notebook = True
            else:
                tc3_reason = f"Object is of type '{notebook_status.object_type}', expected 'NOTEBOOK'."
        except Exception as e:
            tc3_reason = f"Error verifying object type: {e}"

    print_test_case(tc3_name, tc3_status, tc3_score, 5, tc3_reason)

    # ==========================================
    # TC4: Notebook Language Verification (5 points)
    # ==========================================
    tc4_name = "TC4: Notebook Language Verification (PYTHON)"
    tc4_status = "[FAILED]"
    tc4_score = 0
    tc4_reason = "Prerequisite failed."

    if object_is_notebook and notebook_status:
        try:
            from databricks.sdk.service.workspace import Language
            # Compare default language
            if notebook_status.language == Language.PYTHON or str(notebook_status.language).lower() == "python":
                tc4_status = "[PASSED]"
                tc4_score = 5
                tc4_reason = "Notebook default language is configured to PYTHON."
                language_is_python = True
            else:
                tc4_reason = f"Notebook language is '{notebook_status.language}', expected 'PYTHON'."
        except Exception as e:
            tc4_reason = f"Error verifying notebook language: {e}"

    print_test_case(tc4_name, tc4_status, tc4_score, 5, tc4_reason)

    # ==========================================
    # TC5: Interactive Code Check (5 points)
    # ==========================================
    tc5_name = "TC5: Interactive Code Check"
    tc5_status = "[FAILED]"
    tc5_score = 0
    tc5_reason = "Prerequisite failed."

    if language_is_python and client:
        try:
            from databricks.sdk.service.workspace import ExportFormat
            export_resp = client.workspace.export(path=target_notebook, format=ExportFormat.SOURCE)
            content_b64 = export_resp.content
            if content_b64:
                decoded_bytes = base64.b64decode(content_b64)
                source_code = decoded_bytes.decode('utf-8')
                
                # Check for input() function and greeting text
                has_input = "input(" in source_code
                has_message = "Welcome to KodeBuck Databricks Workspace" in source_code
                
                if has_input and has_message:
                    tc5_status = "[PASSED]"
                    tc5_score = 5
                    tc5_reason = "Notebook code successfully prompts for name and prints the welcome greeting."
                else:
                    failures = []
                    if not has_input:
                        failures.append("does not contain 'input()' function call")
                    if not has_message:
                        failures.append("does not contain the greeting string 'Welcome to KodeBuck Databricks Workspace'")
                    tc5_reason = "Notebook code " + " and ".join(failures) + "."
            else:
                tc5_reason = "Notebook source code content is empty."
        except Exception as e:
            tc5_reason = f"Failed to export or verify notebook source: {e}"

    print_test_case(tc5_name, tc5_status, tc5_score, 5, tc5_reason)

    # ==========================================
    # FOOTER
    # ==========================================
    total_score = tc1_score + tc2_score + tc3_score + tc4_score + tc5_score
    print_separator()
    score_string = f"{total_score}/{max_score}"
    print(f"TOTAL SCORE:{score_string:>57}")
    print_separator()

if __name__ == "__main__":
    verify_task()
