import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.pipeline import build_pipeline
from app.graph.workflow import run_query

router = APIRouter()

# In-memory chat history store (per session)
# In production this would be Redis or a DB
chat_sessions: dict = {}


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
    """
    Upload a PDF or TXT document.
    Ingests it into ChromaDB automatically.
    """
    # Validate file type
    allowed = [".pdf", ".txt"]
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed: {allowed}"
        )

    # Save file to data/ folder
    save_path = f"data/{file.filename}"
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    print(f"[Upload] Saved file: {save_path}")

    # Ingest into vector store
    build_pipeline(save_path)

    return UploadResponse(
        message="Document uploaded and ingested successfully!",
        filename=file.filename,
        chunks_info="Document chunked and stored in ChromaDB"
    )


@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    """
    Query the ingested documents.
    Maintains conversation history per session_id.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Get or create session history
    history = chat_sessions.get(request.session_id, [])

    # Run through multi-agent pipeline
    result = run_query(
        query=request.query,
        chat_history=history
    )

    # Update session history
    chat_sessions[request.session_id] = result["chat_history"]

    return QueryResponse(
        query=result["query"],
        refined_query=result["refined_query"],
        answer=result["answer"],
        sources=result["sources"],
        session_id=request.session_id
    )


@router.get("/sessions/{session_id}/history")
async def get_history(session_id: str):
    """
    Get conversation history for a session.
    """
    history = chat_sessions.get(session_id, [])
    return {"session_id": session_id, "history": history}


@router.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """
    Clear conversation history for a session.
    """
    if session_id in chat_sessions:
        del chat_sessions[session_id]
    return {"message": f"Session {session_id} cleared"}