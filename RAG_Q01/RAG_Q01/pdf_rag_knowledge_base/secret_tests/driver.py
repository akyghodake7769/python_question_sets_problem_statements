# import os
# import sys
# import json

# def get_workspace_path():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

# def extract_code_from_workspace():
#     ws = get_workspace_path()
#     combined_code = ""
    
#     # 1. Read from solution.py
#     sol_path = os.path.join(ws, 'solution.py')
#     if os.path.exists(sol_path):
#         try:
#             with open(sol_path, 'r', encoding='utf-8') as f:
#                 lines = f.readlines()
#                 uncommented = "".join(l for l in lines if not l.strip().startswith("#"))
#                 combined_code += "\n\n" + uncommented
#         except Exception:
#             pass

#     # 2. Read from rag_app.py
#     app_path = os.path.join(ws, 'rag_app.py')
#     if os.path.exists(app_path):
#         try:
#             with open(app_path, 'r', encoding='utf-8') as f:
#                 lines = f.readlines()
#                 uncommented = "".join(l for l in lines if not l.strip().startswith("#"))
#                 combined_code += "\n\n" + uncommented
#         except Exception:
#             pass

#     return combined_code

# def run_tests():
#     results = {
#         "tc1": False,
#         "tc2": False,
#         "tc3": False,
#         "tc4": False,
#         "tc5": False
#     }
    
#     ws = get_workspace_path()
#     code = extract_code_from_workspace()
    
#     if not code.strip():
#         return results

#     # TC1: PDF Loading & Processing (5 Marks)
#     has_pypdf = "PyPDFLoader" in code
#     has_load = ".load()" in code or "loader.load" in code
#     results["tc1"] = bool(has_pypdf and has_load)

#     # TC2: Text Chunking (20 Marks)
#     has_splitter = "RecursiveCharacterTextSplitter" in code
#     has_chunk_size = "1000" in code
#     has_overlap = "200" in code
#     results["tc2"] = bool(has_splitter and has_chunk_size and has_overlap)

#     # TC3: Embeddings & ChromaDB (25 Marks)
#     has_embeddings = "text-embedding-3-small" in code or "OpenAIEmbeddings" in code
#     has_chroma = "Chroma" in code and ("from_documents" in code or "persist_directory" in code or "chroma_db" in code)
#     results["tc3"] = bool(has_embeddings and has_chroma)

#     # TC4: Grounded Retrieval & Answer Generation (25 Marks)
#     has_llm = "gpt-4o-mini" in code or "ChatOpenAI" in code
#     has_prompt = "ChatPromptTemplate" in code or "prompt" in code.lower()
#     has_grounding = "could not find the answer" in code.lower() or "only the information" in code.lower() or "only using the provided context" in code.lower()
#     results["tc4"] = bool(has_llm and has_prompt and has_grounding)

#     # TC5: Standalone Interactive Application rag_app.py (25 Marks)
#     app_path = os.path.join(ws, 'rag_app.py')
#     if os.path.exists(app_path):
#         with open(app_path, 'r', encoding='utf-8') as f:
#             app_lines = f.readlines()
#         # Look for uncommented logic
#         active_lines = "".join(l for l in app_lines if not l.strip().startswith("#"))
#         has_loop = "while" in active_lines and "exit" in active_lines.lower()
#         has_input = "input(" in active_lines
#         has_pipeline = "PyPDFLoader" in active_lines and "Chroma" in active_lines and "ChatOpenAI" in active_lines
#         results["tc5"] = bool(has_loop and has_input and has_pipeline)

#     return results

# if __name__ == "__main__":
#     test_results = run_tests()
    
#     TC_NAMES = {
#         "tc1": "Task 1: PDF Loading & PyPDFLoader Processing",
#         "tc2": "Task 2: Text Chunking (RecursiveCharacterTextSplitter 1000/200)",
#         "tc3": "Task 3: Embeddings & ChromaDB Vector Store Persistence",
#         "tc4": "Task 4: Grounded RAG Pipeline & gpt-4o-mini Generation",
#         "tc5": "Task 5: Standalone Interactive rag_app.py Application"
#     }
    
#     TC_MARKS = {
#         "tc1": 5,
#         "tc2": 20,
#         "tc3": 25,
#         "tc4": 25,
#         "tc5": 25
#     }

#     if len(sys.argv) > 1 and sys.argv[1] == '--json':
#         print(json.dumps(test_results))
#     else:
#         print("Running Auto-Evaluation for: PDF-Based Knowledge Base RAG System\n")
#         total_score = 0
#         report_lines = []
#         for k, v in test_results.items():
#             tc_num = k[2:]
#             desc = TC_NAMES.get(k, '')
#             marks = TC_MARKS.get(k, 0)

#             if v:
#                 total_score += marks
#                 msg = f"PASS TC{tc_num} [{desc}] ({marks}/{marks})"
#             else:
#                 msg = f"FAIL TC{tc_num} [{desc}] (0/{marks})"
            
#             print(msg)
#             report_lines.append(msg)
            
#         score_summary = f"\nSCORE: {total_score}/100.0"
#         print(score_summary)
#         report_lines.append(score_summary)

#         # Write to report.txt in student workspace
#         try:
#             ws = get_workspace_path()
#             with open(os.path.join(ws, 'report.txt'), 'w', encoding='utf-8') as f:
#                 f.write("\n".join(report_lines) + "\n")
#         except Exception:
#             pass

import os
import sys
import json
import datetime

def get_workspace_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def extract_code_from_workspace(solution_path=None):
    ws = get_workspace_path()
    combined_code = ""
    
    # 1. Read from specified solution_path if provided
    if solution_path and os.path.exists(solution_path):
        try:
            with open(solution_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                uncommented = "".join(l for l in lines if not l.strip().startswith("#"))
                combined_code += "\n\n" + uncommented
        except Exception:
            pass

    # 2. Read from default student_workspace/solution.py
    sol_path = os.path.join(ws, 'solution.py')
    if (not solution_path or not os.path.exists(solution_path)) and os.path.exists(sol_path):
        try:
            with open(sol_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                uncommented = "".join(l for l in lines if not l.strip().startswith("#"))
                combined_code += "\n\n" + uncommented
        except Exception:
            pass

    # 3. Read from rag_app.py (either next to solution_path or in student_workspace)
    app_candidates = []
    if solution_path:
        app_candidates.append(os.path.join(os.path.dirname(os.path.abspath(solution_path)), 'rag_app.py'))
    app_candidates.append(os.path.join(ws, 'rag_app.py'))

    for app_path in app_candidates:
        if os.path.exists(app_path):
            try:
                with open(app_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    uncommented = "".join(l for l in lines if not l.strip().startswith("#"))
                    combined_code += "\n\n" + uncommented
                    break
            except Exception:
                pass

    return combined_code

def run_tests(solution_path=None):
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False,
        "tc4": False,
        "tc5": False
    }
    
    ws = get_workspace_path()
    code = extract_code_from_workspace(solution_path)
    
    if not code.strip():
        return results

    # TC1: PDF Loading & Processing (5 Marks)
    has_pypdf = "PyPDFLoader" in code
    has_load = ".load()" in code or "loader.load" in code
    results["tc1"] = bool(has_pypdf and has_load)

    # TC2: Text Chunking (20 Marks)
    has_splitter = "RecursiveCharacterTextSplitter" in code
    has_chunk_size = "1000" in code
    has_overlap = "200" in code
    results["tc2"] = bool(has_splitter and has_chunk_size and has_overlap)

    # TC3: Embeddings & ChromaDB (25 Marks)
    has_embeddings = "text-embedding-3-small" in code or "OpenAIEmbeddings" in code
    has_chroma = "Chroma" in code and ("from_documents" in code or "persist_directory" in code or "chroma_db" in code)
    results["tc3"] = bool(has_embeddings and has_chroma)

    # TC4: Grounded Retrieval & Answer Generation (25 Marks)
    has_llm = "gpt-4o-mini" in code or "ChatOpenAI" in code
    has_prompt = "ChatPromptTemplate" in code or "prompt" in code.lower()
    has_grounding = "could not find the answer" in code.lower() or "only the information" in code.lower() or "only using the provided context" in code.lower()
    results["tc4"] = bool(has_llm and has_prompt and has_grounding)

    # TC5: Standalone Interactive Application rag_app.py (25 Marks)
    app_candidates = []
    if solution_path:
        app_candidates.append(os.path.join(os.path.dirname(os.path.abspath(solution_path)), 'rag_app.py'))
    app_candidates.append(os.path.join(ws, 'rag_app.py'))

    for app_path in app_candidates:
        if os.path.exists(app_path):
            try:
                with open(app_path, 'r', encoding='utf-8') as f:
                    app_lines = f.readlines()
                active_lines = "".join(l for l in app_lines if not l.strip().startswith("#"))
                has_loop = "while" in active_lines and "exit" in active_lines.lower()
                has_input = "input(" in active_lines
                has_pipeline = "PyPDFLoader" in active_lines and "Chroma" in active_lines and "ChatOpenAI" in active_lines
                results["tc5"] = bool(has_loop and has_input and has_pipeline)
                break
            except Exception:
                pass

    # If code contains all Task 5 logic inside solution_path itself
    if not results["tc5"]:
        has_loop = "while" in code and "exit" in code.lower()
        has_input = "input(" in code
        has_pipeline = "PyPDFLoader" in code and "Chroma" in code and "ChatOpenAI" in code
        results["tc5"] = bool(has_loop and has_input and has_pipeline)

    return results

def test_student_code(solution_path=None, vm_tag="LOCAL_VM", exam_code="RAG_EXAM"):
    test_results = run_tests(solution_path)
    
    TC_MARKS = {
        "tc1": 5,
        "tc2": 20,
        "tc3": 25,
        "tc4": 25,
        "tc5": 25
    }
    
    total_score = sum(TC_MARKS[k] for k, v in test_results.items() if v)
    total_possible = sum(TC_MARKS.values())

    tc_strings = []
    for k, v in test_results.items():
        marks = TC_MARKS[k]
        if v:
            tc_strings.append(f"{k.upper()}: PASSED ({marks})")
        else:
            tc_strings.append(f"{k.upper()}: FAILED (0)")

    # Format standard KodeBuck Telemetry line
    now = datetime.datetime.now()
    date_str = now.strftime('%d-%m-%Y')
    time_str = now.strftime('%Y%m%d_%H%M%S')
    
    csv_line = f"{date_str},RAG_Q01_M,{vm_tag},{exam_code},{time_str},{'; '.join(tc_strings)},{total_score},{total_possible}"
    
    print("=" * 60)
    print(f"KODEBUCK EVALUATION COMPLETED: {total_score}/{total_possible}")
    print("=" * 60)
    print(f"\n[REPORT_CSV]{csv_line}")
    return test_results

if __name__ == "__main__":
    target_sol = None
    if len(sys.argv) > 1 and sys.argv[1] != '--json':
        target_sol = sys.argv[1]

    test_results = run_tests(target_sol)
    
    TC_NAMES = {
        "tc1": "Task 1: PDF Loading & PyPDFLoader Processing",
        "tc2": "Task 2: Text Chunking (RecursiveCharacterTextSplitter 1000/200)",
        "tc3": "Task 3: Embeddings & ChromaDB Vector Store Persistence",
        "tc4": "Task 4: Grounded RAG Pipeline & gpt-4o-mini Generation",
        "tc5": "Task 5: Standalone Interactive rag_app.py Application"
    }
    
    TC_MARKS = {
        "tc1": 5,
        "tc2": 20,
        "tc3": 25,
        "tc4": 25,
        "tc5": 25
    }

    if '--json' in sys.argv:
        print(json.dumps(test_results))
    else:
        print("Running Auto-Evaluation for: PDF-Based Knowledge Base RAG System\n")
        total_score = 0
        report_lines = []
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = TC_MARKS.get(k, 0)

            if v:
                total_score += marks
                msg = f"PASS TC{tc_num} [{desc}] ({marks}/{marks})"
            else:
                msg = f"FAIL TC{tc_num} [{desc}] (0/{marks})"
            
            print(msg)
            report_lines.append(msg)
            
        score_summary = f"\nSCORE: {total_score}/100.0"
        print(score_summary)
        report_lines.append(score_summary)

        # Write to report.txt in student workspace
        try:
            ws = get_workspace_path()
            with open(os.path.join(ws, 'report.txt'), 'w', encoding='utf-8') as f:
                f.write("\n".join(report_lines) + "\n")
        except Exception:
            pass
