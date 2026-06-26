from app.core.ingestion import ingest_document
from app.core.vectorstore import add_documents_to_vectorstore, get_retriever
from langchain_core.documents import Document
from typing import List


def build_pipeline(file_path: str) -> None:
    """
    Full ingestion pipeline:
    Load document → chunk → embed → store in ChromaDB
    Call this once when a new document is uploaded.
    """
    print(f"\n[Pipeline] Starting ingestion for: {file_path}")
    
    # Step 1 - Load and chunk
    chunks = ingest_document(file_path)
    
    # Step 2 - Embed and store
    add_documents_to_vectorstore(chunks)
    
    print(f"[Pipeline] ✅ Document ready for querying!\n")


def query_pipeline(query: str, k: int = 4) -> List[Document]:
    """
    Query pipeline:
    User query → embed → search ChromaDB → return top-k chunks
    """
    print(f"\n[Pipeline] Searching for: '{query}'")
    
    retriever = get_retriever(k=k)
    results = retriever.invoke(query)
    
    print(f"[Pipeline] ✅ Found {len(results)} relevant chunks\n")
    return results