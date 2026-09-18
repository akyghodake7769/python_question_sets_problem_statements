# Guided Project: PDF-Based Knowledge Base RAG System

Duration: 60 Min.

## Scenario

Build a complete Retrieval-Augmented Generation (RAG) pipeline using LangChain, OpenAI (`text-embedding-3-small` and `gpt-4o-mini`), and ChromaDB. The system must ingest an employee handbook PDF, create vector embeddings, retrieve relevant context, and provide context-grounded answers while refusing to hallucinate when asked questions outside the document.

## Target File Location & Creation

- **Notebook**: `student_workspace/Participant_Problem.ipynb` (Complete Tasks 1 to 5)
- **Application File**: `student_workspace/rag_app.py` (Complete standalone interactive application)
- **Source Document**: `student_workspace/04_DATA/sample_knowledge_base.pdf`

## Required Pipeline

**PDF → PyPDFLoader → RecursiveCharacterTextSplitter (1000/200) → text-embedding-3-small → ChromaDB → Retriever (Top-3) → GPT-4o-mini → Grounded Answer + Source Page**

## Instructions to Perform the Task

1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files under `student_workspace/`.
2. Open `Participant_Problem.ipynb` and follow the guided step-by-step tasks.
3. Complete Task 1 (Document Loading), Task 2 (Chunking), Task 3 (Embeddings & ChromaDB), and Task 4 (RAG Pipeline).
4. Assemble the complete standalone interactive CLI application in `rag_app.py` (Task 5) with loop and `exit` condition.
5. Save your changes (`Ctrl + S` or `Cmd + S`).
6. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
7. Verify your progress by running `python run.py` locally in the terminal.
8. Once all test cases pass, return to the platform dashboard and click the **"Run Test" / "Verify"** button.

## Validation & Scoring Rubric

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                                                                                         | Marks    |
| :------------ | :------------------------------------------------------------------------------------------------------------------ | :------- |
| **TC1** | **Task 1: PDF Loading & Processing** (`PyPDFLoader`, extracts 15 pages, preserves metadata)                 | 5 Marks  |
| **TC2** | **Task 2: Text Chunking** (`RecursiveCharacterTextSplitter`, `chunk_size=1000`, `chunk_overlap=200`)    | 20 Marks |
| **TC3** | **Task 3: Embeddings & ChromaDB** (`text-embedding-3-small`, Chroma persistence, similarity search)         | 25 Marks |
| **TC4** | **Task 4: Grounded RAG Pipeline** (Top-3 retrieval, `gpt-4o-mini`, grounded prompt, exact refusal fallback) | 25 Marks |
| **TC5** | **Task 5: Final Interactive App (`rag_app.py`)** (Complete CLI loop, answers queries, handles exit)         | 25 Marks |

**Total Score: 100 Marks**

## Important Notes

- This is an auto-evaluated question. Ensure all code edits are properly saved and the `run.py` checks pass before submission.
- Do not modify files in `secret_tests/` or change directory structures under `student_workspace/`.
