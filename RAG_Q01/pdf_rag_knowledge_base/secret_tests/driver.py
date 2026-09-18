import os
import sys
import json
import nbformat

def get_workspace_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def extract_code_from_workspace():
    ws = get_workspace_path()
    combined_code = ""
    
    # 1. Read from Participant_Problem.ipynb
    nb_path = os.path.join(ws, 'Participant_Problem.ipynb')
    if os.path.exists(nb_path):
        try:
            nb = nbformat.read(nb_path, as_version=4)
            code_cells = [c.source for c in nb.cells if c.cell_type == 'code']
            combined_code += "\n\n" + "\n\n".join(code_cells)
        except Exception:
            pass

    # 2. Read from rag_app.py
    app_path = os.path.join(ws, 'rag_app.py')
    if os.path.exists(app_path):
        try:
            with open(app_path, 'r', encoding='utf-8') as f:
                # Exclude full line comments for code checking
                lines = f.readlines()
                uncommented = "".join(l for l in lines if not l.strip().startswith("#"))
                combined_code += "\n\n" + uncommented
        except Exception:
            pass

    return combined_code

def run_tests():
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False,
        "tc4": False,
        "tc5": False
    }
    
    ws = get_workspace_path()
    code = extract_code_from_workspace()
    
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
    app_path = os.path.join(ws, 'rag_app.py')
    if os.path.exists(app_path):
        with open(app_path, 'r', encoding='utf-8') as f:
            app_lines = f.readlines()
        # Look for uncommented logic
        active_lines = "".join(l for l in app_lines if not l.strip().startswith("#"))
        has_loop = "while" in active_lines and "exit" in active_lines.lower()
        has_input = "input(" in active_lines
        has_pipeline = "PyPDFLoader" in active_lines and "Chroma" in active_lines and "ChatOpenAI" in active_lines
        results["tc5"] = bool(has_loop and has_input and has_pipeline)

    return results

if __name__ == "__main__":
    test_results = run_tests()
    
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

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
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
