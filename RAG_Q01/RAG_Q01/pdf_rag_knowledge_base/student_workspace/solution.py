"""
Guided Project: PDF-Based Knowledge Base RAG System
Solution Script: solution.py (Tasks 1 to 4)

Complete the tasks below in order:
- Task 1: Load PDF with PyPDFLoader
- Task 2: Chunk text with RecursiveCharacterTextSplitter (chunk_size=1000, chunk_overlap=200)
- Task 3: Embeddings (text-embedding-3-small) and ChromaDB persistence
- Task 4: Build Grounded RAG Question-Answering Pipeline (gpt-4o-mini, refusal fallback)
"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

PDF_PATH = "04_DATA/sample_knowledge_base.pdf"
CHROMA_PATH = "./chroma_db"


# ==============================================================================
# Task 1: Load the PDF
# ==============================================================================
def load_pdf_document(file_path=PDF_PATH):
    """
    Load the supplied PDF using LangChain's PyPDFLoader.
    Returns: list of Document objects.
    """
    # TODO: Create the PyPDFLoader instance and load documents
    # loader = PyPDFLoader(file_path)
    # documents = loader.load()
    # return documents
    pass


# ==============================================================================
# Task 2: Split the Document into Chunks
# ==============================================================================
def split_documents_into_chunks(documents, chunk_size=1000, chunk_overlap=200):
    """
    Split the loaded documents into fixed-size chunks using RecursiveCharacterTextSplitter.
    Returns: list of Document chunks.
    """
    # TODO: Create RecursiveCharacterTextSplitter with chunk_size=1000, chunk_overlap=200
    # splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    # chunks = splitter.split_documents(documents)
    # return chunks
    pass


# ==============================================================================
# Task 3: Generate Embeddings and Store in ChromaDB
# ==============================================================================
def create_vector_store(chunks, persist_dir=CHROMA_PATH):
    """
    Generate embeddings using 'text-embedding-3-small' and store chunks in ChromaDB.
    Returns: Chroma vector store instance.
    """
    # TODO: Initialize OpenAIEmbeddings and create Chroma vectorstore from documents
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    # vectorstore = Chroma.from_documents(
    #     documents=chunks,
    #     embedding=embeddings,
    #     persist_directory=persist_dir
    # )
    # return vectorstore
    pass


# ==============================================================================
# Task 4: Build Grounded RAG Question-Answering Pipeline
# ==============================================================================
def build_rag_pipeline(vectorstore, question="What is the purpose of this document?"):
    """
    Connect ChromaDB retrieval to GPT-4o-mini with grounded refusal prompt.
    Returns: generated answer string.
    """
    # TODO: Create retriever with search_kwargs={"k": 3}
    # retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    #
    # TODO: Initialize ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    #
    # TODO: Define grounded prompt template
    # prompt = ChatPromptTemplate.from_template('''
    # You are a PDF question-answering assistant.
    # Answer ONLY using the provided context.
    # Do not use outside knowledge.
    # If the answer is not available in the context, say:
    # "I could not find the answer in the provided document."
    #
    # Context:
    # {context}
    #
    # Question:
    # {question}
    #
    # Answer:
    # ''')
    #
    # retrieved_docs = retriever.invoke(question)
    # context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    # chain = prompt | llm
    # response = chain.invoke({"context": context, "question": question})
    # return response.content
    pass


def main():
    print("=== Running RAG Knowledge Base Pipeline ===")
    if not os.path.exists(PDF_PATH):
        print(f"Warning: PDF file not found at {PDF_PATH}")

    # Step 1: Load PDF
    # documents = load_pdf_document(PDF_PATH)
    # print(f"Loaded {len(documents)} pages.")

    # Step 2: Split into chunks
    # chunks = split_documents_into_chunks(documents)
    # print(f"Created {len(chunks)} chunks.")

    # Step 3: Embeddings & Vector Store
    # vectorstore = create_vector_store(chunks)
    # print("Vector store created successfully.")

    # Step 4: Run Sample RAG Query
    # answer = build_rag_pipeline(vectorstore, "What is the purpose of this document?")
    # print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
