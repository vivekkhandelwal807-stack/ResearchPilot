import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.core.embeddings import get_embedding_model
from typing import List

CHROMA_DIR = "chroma_db"  # where ChromaDB will persist data

def get_vectorstore() -> Chroma:
    """
    Connect to existing ChromaDB vector store.
    """
    embedding_model = get_embedding_model()
    vectorstore = Chroma(
        collection_name="rag_documents",
        embedding_function=embedding_model,
        persist_directory=CHROMA_DIR
    )
    return vectorstore


def add_documents_to_vectorstore(chunks: List[Document]) -> Chroma:
    """
    Embed chunks and store them in ChromaDB.
    """
    embedding_model = get_embedding_model()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name="rag_documents",
        persist_directory=CHROMA_DIR
    )
    print(f"[VectorStore] Stored {len(chunks)} chunks in ChromaDB")
    return vectorstore


def get_retriever(k: int = 4):
    """
    Returns a retriever that fetches top-k similar chunks.
    k=4 means we get 4 most relevant chunks per query.
    """
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    print(f"[VectorStore] Retriever ready — fetching top {k} chunks")
    return retriever