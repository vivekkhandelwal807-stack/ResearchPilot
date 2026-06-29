import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.pipeline import build_pipeline
from app.graph.workflow import run_query
from app.core.database import (
    save_session, load_session, delete_session,
    save_document, get_all_documents, get_all_sessions
)

router = APIRouter()


# ---- Request/Response Models ----

class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"


class QueryResponse(BaseModel):
    query: str
    refined_query: str
    answer: str
    sources: List[str]
    session_id: str


class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_info: str


# ---- Endpoints ----

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    allowed = [".pdf", ".txt"]
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed: {allowed}"
        )

    save_path = f"data/{file.filename}"
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    print(f"[Upload] Saved file: {save_path}")

    # Ingest into vector store
    build_pipeline(save_path)

    # Save document record to SQLite
    save_document(file.filename, save_path)

    return UploadResponse(
        message="Document uploaded and ingested successfully!",
        filename=file.filename,
        chunks_info="Document chunked and stored in ChromaDB"
    )


@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Load history from SQLite
    history = load_session(request.session_id)

    # Run through multi-agent pipeline
    result = run_query(
        query=request.query,
        chat_history=history
    )

    # Save updated history to SQLite
    save_session(request.session_id, result["chat_history"])

    return QueryResponse(
        query=result["query"],
        refined_query=result["refined_query"],
        answer=result["answer"],
        sources=result["sources"],
        session_id=request.session_id
    )


@router.get("/sessions/{session_id}/history")
async def get_history(session_id: str):
    history = load_session(session_id)
    return {"session_id": session_id, "history": history}


@router.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    delete_session(session_id)
    return {"message": f"Session {session_id} cleared"}


@router.get("/sessions")
async def list_sessions():
    """Get all active sessions."""
    sessions = get_all_sessions()
    return {"sessions": sessions}


@router.get("/documents")
async def list_documents():
    """Get all uploaded documents."""
    docs = get_all_documents()
    return {"documents": docs}