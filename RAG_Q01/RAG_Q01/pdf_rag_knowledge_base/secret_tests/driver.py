import os
import sys
import json
import ast

def get_workspace_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def get_clean_uncommented_code(file_path):
    if not file_path or not os.path.exists(file_path):
        return ""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            uncommented = "".join(l for l in lines if not l.strip().startswith("#"))
            return uncommented
    except Exception:
        return ""

def get_ast_function_bodies(source_code):
    funcs = {}
    if not source_code.strip():
        return funcs
    try:
        tree = ast.parse(source_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                non_trivial = [
                    s for s in node.body 
                    if not (isinstance(s, ast.Pass)) 
                    and not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))
                ]
                funcs[node.name] = (node, non_trivial)
    except Exception:
        pass
    return funcs

def run_tests(solution_path=None):
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False,
        "tc4": False,
        "tc5": False
    }

    ws = get_workspace_path()

    # Determine student solution.py and rag_app.py file paths separately
    if solution_path and os.path.exists(solution_path):
        sol_file = os.path.abspath(solution_path)
        dir_path = os.path.dirname(sol_file)
        app_file = os.path.join(dir_path, 'rag_app.py')
        if not os.path.exists(app_file):
            app_file = os.path.join(ws, 'rag_app.py')
    else:
        sol_file = os.path.join(ws, 'solution.py')
        app_file = os.path.join(ws, 'rag_app.py')

    sol_code = get_clean_uncommented_code(sol_file)
    app_code = get_clean_uncommented_code(app_file)

    sol_funcs = get_ast_function_bodies(sol_code)
    app_funcs = get_ast_function_bodies(app_code)

    # -------------------------------------------------------------------------
    # TC1: Task 1: PDF Loading & PyPDFLoader Processing (5 Marks)
    # Evaluated strictly from solution.py
    # -------------------------------------------------------------------------
    if sol_code:
        has_loader = "PyPDFLoader" in sol_code
        has_load_call = ".load()" in sol_code or "load(" in sol_code
        fn1 = sol_funcs.get("load_pdf_document")
        has_body = (fn1 is not None and len(fn1[1]) > 0) or ("PyPDFLoader(" in sol_code and has_load_call)
        results["tc1"] = bool(has_loader and has_load_call and has_body)

    # -------------------------------------------------------------------------
    # TC2: Task 2: Text Chunking (RecursiveCharacterTextSplitter 1000/200) (20 Marks)
    # Evaluated strictly from solution.py
    # -------------------------------------------------------------------------
    if sol_code:
        has_splitter = "RecursiveCharacterTextSplitter" in sol_code
        has_split_call = ".split_documents" in sol_code or "split_documents(" in sol_code or ".split_text" in sol_code
        fn2 = sol_funcs.get("split_documents_into_chunks")
        has_body = (fn2 is not None and len(fn2[1]) > 0) or ("RecursiveCharacterTextSplitter(" in sol_code and has_split_call)
        results["tc2"] = bool(has_splitter and has_split_call and has_body)

    # -------------------------------------------------------------------------
    # TC3: Task 3: Embeddings & ChromaDB Vector Store Persistence (25 Marks)
    # Evaluated strictly from solution.py
    # -------------------------------------------------------------------------
    if sol_code:
        has_embed = "OpenAIEmbeddings" in sol_code or "text-embedding-3-small" in sol_code
        has_chroma = "Chroma" in sol_code
        has_store = "from_documents" in sol_code or "persist_directory" in sol_code or "persist_dir" in sol_code
        fn3 = sol_funcs.get("create_vector_store")
        has_body = (fn3 is not None and len(fn3[1]) > 0) or ("Chroma.from_documents" in sol_code or "from_documents(" in sol_code)
        results["tc3"] = bool(has_embed and has_chroma and has_store and has_body)

    # -------------------------------------------------------------------------
    # TC4: Task 4: Grounded RAG Pipeline & gpt-4o-mini Generation (25 Marks)
    # Evaluated strictly from solution.py
    # -------------------------------------------------------------------------
    if sol_code:
        has_llm = "gpt-4o-mini" in sol_code or "ChatOpenAI" in sol_code
        has_retriever = "as_retriever" in sol_code or "retriever" in sol_code
        has_prompt = "ChatPromptTemplate" in sol_code or "prompt" in sol_code.lower()
        has_grounding = (
            "could not find the answer" in sol_code.lower() or 
            "only using the provided context" in sol_code.lower() or 
            "only the information" in sol_code.lower() or
            "not available in the context" in sol_code.lower()
        )
        fn4 = sol_funcs.get("build_rag_pipeline")
        has_body = (fn4 is not None and len(fn4[1]) > 0) or ("invoke(" in sol_code and has_grounding)
        results["tc4"] = bool(has_llm and has_retriever and has_prompt and has_grounding and has_body)

    # -------------------------------------------------------------------------
    # TC5: Task 5: Standalone Interactive rag_app.py Application (25 Marks)
    # Evaluated strictly from rag_app.py (Must NOT be satisfied by solution.py)
    # -------------------------------------------------------------------------
    if app_code:
        has_loop = "while" in app_code and ("exit" in app_code.lower() or "break" in app_code or "sys.exit" in app_code)
        has_input = "input(" in app_code
        has_pipeline = (
            ("PyPDFLoader" in app_code or "load(" in app_code) and
            ("Chroma" in app_code or "vectorstore" in app_code) and
            ("ChatOpenAI" in app_code or "gpt-4o-mini" in app_code)
        )
        app_main = app_funcs.get("main")
        has_active_logic = False
        if app_main is not None:
            real_stmts = [
                s for s in app_main[1] 
                if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Call) and getattr(s.value.func, 'id', '') == 'print')
            ]
            if len(real_stmts) > 0:
                has_active_logic = True
        elif has_loop and has_input and has_pipeline:
            has_active_logic = True

        results["tc5"] = bool(has_loop and has_input and has_pipeline and has_active_logic)

    return results

def verify_task_central(username="LOCAL_VM", start_time_str=None, exam_code="UNKNOWN", **kwargs):
    solution_path = kwargs.get('solution_path')
    from driver import verify_task_central as _vtc
    return _vtc(username=username, start_time_str=start_time_str, exam_code=exam_code, solution_path=solution_path)

def test_student_code(solution_path=None, vm_tag="LOCAL_VM", exam_code="RAG_EXAM"):
    return verify_task_central(username=vm_tag, exam_code=exam_code, solution_path=solution_path)

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
