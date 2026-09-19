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
