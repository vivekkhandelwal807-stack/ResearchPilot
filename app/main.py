from fastapi import FastAPI
from app.api.routes import router
from app.core.database import init_db

app = FastAPI(
    title="Multi-Agent RAG Research Assistant",
    description="Intelligent document analysis using LangGraph + LangChain + Groq",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "RAG Research Assistant is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}