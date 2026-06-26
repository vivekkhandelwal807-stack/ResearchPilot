import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List


def load_document(file_path: str) -> List[Document]:
    """
    Load a document from a file path.
    Supports PDF and TXT files.
    """
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    documents = loader.load()
    print(f"[Ingestion] Loaded {len(documents)} page(s) from {file_path}")
    return documents


def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into overlapping chunks for better retrieval.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,        # ~800 characters per chunk
        chunk_overlap=150,     # 150 characters overlap between chunks
        separators=["\n\n", "\n", ".", " "]  # split priority order
    )

    chunks = splitter.split_documents(documents)
    print(f"[Ingestion] Created {len(chunks)} chunks")
    return chunks


def ingest_document(file_path: str) -> List[Document]:
    """
    Full pipeline: load → chunk
    Returns chunks ready for embedding.
    """
    documents = load_document(file_path)
    chunks = chunk_documents(documents)
    return chunks