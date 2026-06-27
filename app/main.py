from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Multi-Agent RAG Research Assistant",
    description="Intelligent document analysis using LangGraph + LangChain + Gemini",
    version="1.0.0"
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "RAG Research Assistant is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}