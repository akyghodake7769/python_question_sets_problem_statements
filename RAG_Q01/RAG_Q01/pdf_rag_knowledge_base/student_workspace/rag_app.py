"""
Guided Project: PDF-Based Knowledge Base RAG System
Task 5: Complete Interactive Application (rag_app.py)

Implement the full end-to-end RAG pipeline here:
1. Load PDF from '04_DATA/sample_knowledge_base.pdf' using PyPDFLoader
2. Split documents with RecursiveCharacterTextSplitter (chunk_size=1000, chunk_overlap=200)
3. Generate embeddings with OpenAIEmbeddings (text-embedding-3-small)
4. Store in ChromaDB vector store (persist_directory='../chroma_db' or './chroma_db')
5. Create retriever with search_kwargs={'k': 3}
6. Initialize ChatOpenAI(model='gpt-4o-mini', temperature=0)
7. Create grounded ChatPromptTemplate
8. Interactive CLI query loop with while True and exit condition
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

PDF_PATH = "04_DATA/sample_knowledge_base.pdf"
CHROMA_PATH = "./chroma_db"

def main():
    # TODO: Step 1 - Load PDF
    # loader = PyPDFLoader(PDF_PATH)
    # documents = loader.load()

    # TODO: Step 2 - Chunk documents
    # splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # chunks = splitter.split_documents(documents)

    # TODO: Step 3 - Generate Embeddings & ChromaDB Vector Store
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    # vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_PATH)

    # TODO: Step 4 - Create Retriever
    # retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # TODO: Step 5 - Initialize LLM
    # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # TODO: Step 6 - Create Grounded Prompt Template
    # prompt = ChatPromptTemplate.from_template('''
    # You are a PDF question-answering assistant.
    # Answer ONLY using the provided context.
    # Do not use outside knowledge.
    # If the answer is not available in the context, say:
    # "I could not find the answer in the provided document."
    # Context:
    # {context}
    # Question:
    # {question}
    # Answer:
    # ''')

    # TODO: Step 7 - Interactive QA Loop
    print("PDF RAG System Ready. Type your question or 'exit' to quit.")
    # while True:
    #     question = input("\nAsk a question (type exit to stop): ")
    #     if question.lower() == "exit":
    #         break
    #     ...

if __name__ == "__main__":
    main()

# """
# Guided Project: PDF-Based Knowledge Base RAG System
# Reference Solution: rag_app_reference.py (Task 5)
# FOR INTERNAL TESTING / REFERENCE ONLY. NOT FOR PARTICIPANTS.

# Complete standalone interactive application implementing the full RAG pipeline:
# 1. Load PDF from '04_DATA/sample_knowledge_base.pdf' using PyPDFLoader
# 2. Split documents with RecursiveCharacterTextSplitter (chunk_size=1000, chunk_overlap=200)
# 3. Generate embeddings with OpenAIEmbeddings (text-embedding-3-small)
# 4. Store in ChromaDB vector store (persist_directory='./chroma_db')
# 5. Create retriever with search_kwargs={'k': 3}
# 6. Initialize ChatOpenAI(model='gpt-4o-mini', temperature=0)
# 7. Create grounded ChatPromptTemplate with exact refusal fallback
# 8. Interactive CLI query loop with while True and exit condition
# """

# import os
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_chroma import Chroma
# from langchain_core.prompts import ChatPromptTemplate

# # Base Paths (handles running from secret_tests or student_workspace)
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../student_workspace"))
# PDF_PATH = os.path.join(BASE_DIR, "04_DATA", "sample_knowledge_base.pdf")
# if not os.path.exists(PDF_PATH):
#     PDF_PATH = "04_DATA/sample_knowledge_base.pdf"

# CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
# if not os.path.exists(os.path.dirname(CHROMA_PATH)):
#     CHROMA_PATH = "./chroma_db"


# def main():
#     # 1. Load PDF
#     loader = PyPDFLoader(PDF_PATH)
#     documents = loader.load()
#     print(f"Loaded {len(documents)} pages from PDF.")

#     # 2. Chunk Documents
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200
#     )
#     chunks = splitter.split_documents(documents)
#     print(f"Created {len(chunks)} text chunks.")

#     # 3. Generate Embeddings & ChromaDB Vector Store
#     embeddings = OpenAIEmbeddings(
#         model="text-embedding-3-small"
#     )
#     vectorstore = Chroma.from_documents(
#         documents=chunks,
#         embedding=embeddings,
#         persist_directory=CHROMA_PATH
#     )
#     print("Vector store initialized successfully.")

#     # 4. Create Retriever
#     retriever = vectorstore.as_retriever(
#         search_kwargs={"k": 3}
#     )

#     # 5. Initialize LLM
#     llm = ChatOpenAI(
#         model="gpt-4o-mini",
#         temperature=0
#     )

#     # 6. Create Grounded Prompt Template
#     prompt = ChatPromptTemplate.from_template(
#         """
# You are a PDF question-answering assistant.

# Answer ONLY using the provided context.
# Do not use outside knowledge.

# If the answer is not available in the context, say:
# "I could not find the answer in the provided document."

# Context:
# {context}

# Question:
# {question}

# Answer:
# """
#     )

#     # 7. Interactive QA Loop
#     print("\n=======================================================")
#     print("PDF RAG System Ready. Type your question or 'exit' to quit.")
#     print("=======================================================")

#     while True:
#         try:
#             question = input("\nAsk a question (type exit to stop): ").strip()
#         except (EOFError, KeyboardInterrupt):
#             print("\nExiting interactive application. Goodbye!")
#             break

#         if not question:
#             continue

#         if question.lower() == "exit":
#             print("Exiting interactive application. Goodbye!")
#             break

#         retrieved_docs = retriever.invoke(question)

#         context = "\n\n".join(
#             doc.page_content for doc in retrieved_docs
#         )

#         messages = prompt.format_messages(
#             context=context,
#             question=question
#         )

#         response = llm.invoke(messages)

#         print("\nAnswer:")
#         print(response.content)

#         print("\nSources:")
#         for doc in retrieved_docs:
#             print("Page:", doc.metadata.get("page", "Unknown"))


# if __name__ == "__main__":
#     main()

