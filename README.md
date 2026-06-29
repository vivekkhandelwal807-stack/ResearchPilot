#  RAG Research Assistant

> Upload any document. Ask questions. Get accurate answers with sources — powered by multiple AI agents working together.



##  What is this project?

Imagine having a research assistant that can read any document you give it and answer your questions intelligently — not just by searching keywords, but by actually *understanding* the content.

That's what this project does.

You upload a PDF or text file. The system processes it, breaks it into meaningful chunks, and stores it in a vector database. When you ask a question, three AI agents collaborate to give you the best possible answer with citations.



##  How the AI Agents Work Together

Instead of sending your question directly to an AI model, this system uses **three specialized agents** that pass work to each other like a relay race:

**Agent 1 — The Query Planner **
Takes your raw question (even with typos or vague phrasing) and rewrites it into a clear, retrieval-friendly query.

> *"wat is rag?" → "What is Retrieval Augmented Generation and how does it work?"*

**Agent 2 — The Retriever **
Searches the vector database and pulls the most relevant chunks from your document using semantic similarity — not just keyword matching.

**Agent 3 — The Reasoner **
Reads the retrieved chunks, reasons over them, and writes a clear answer with source citations so you know exactly where the information came from.



##  Key Features

-  **Upload any PDF or TXT** and start asking questions instantly
-  **Multi-agent pipeline** built with LangGraph for intelligent query handling
-  **Semantic search** finds relevant content even when you don't use exact keywords
-  **Citations in every answer** so you can verify information
-  **Conversational memory** remembers your previous questions in the same session
-  **Persistent sessions** — chat history survives even if the server restarts
-  **Clean web interface** built with Streamlit
-  **REST API** with full Swagger documentation for developers
-  **Docker ready** for easy deployment anywhere



##  Built With

| What | Why |
|------|-----|
| **LangGraph** | Orchestrates the multi-agent workflow |
| **LangChain** | Handles LLM chains and document processing |
| **Groq + Llama 4** | Fast, free LLM for reasoning and planning |
| **HuggingFace Embeddings** | Converts text to vectors locally (no API cost) |
| **ChromaDB** | Stores and searches document vectors persistently |
| **FastAPI** | Powers the backend REST API |
| **Streamlit** | Provides the interactive web interface |
| **SQLite** | Persists chat sessions across server restarts |
| **Docker** | Packages everything for consistent deployment |



##  Getting Started

### What you need
- Python 3.11+
- A free Groq API key from [console.groq.com](https://console.groq.com)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/vivekkhandelwal807-stack/ResearchPilot.git
cd ResearchPilot

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env
# Open .env and add your Groq API key

# 5. Start the API server
uvicorn app.main:app --reload --port 8000

# 6. Start the frontend (new terminal)
streamlit run frontend/app.py
```

Then open **http://localhost:8501** in your browser and start chatting with your documents!

---

##  Run with Docker

If you have Docker installed, one command runs everything:

```bash
docker-compose up --build
```

- Frontend → http://localhost:8501
- API docs → http://localhost:8000/docs

---

##  API Endpoints

| Endpoint | What it does |
|----------|-------------|
| `POST /api/upload` | Upload and process a document |
| `POST /api/query` | Ask a question about your documents |
| `GET /api/sessions/{id}/history` | View past conversation |
| `DELETE /api/sessions/{id}` | Clear a conversation |
| `GET /api/documents` | See all uploaded documents |
| `GET /health` | Check if API is running |

Full interactive API docs available at **http://localhost:8000/docs**

---

##  How to Use

1. **Upload** a PDF or TXT file from the sidebar
2. **Click Ingest** — the system processes and indexes your document
3. **Ask anything** about the document in the chat
4. **Get answers** with source citations
5. **Ask follow-ups** — the system remembers your conversation
6. **Download** your chat history anytime

---

##  Project Structure

ResearchPilot/

├── app/

│   ├── agents/          # The three AI agents

│   ├── core/            # RAG pipeline, embeddings, database

│   ├── graph/           # LangGraph workflow and state

│   └── api/             # FastAPI routes

├── frontend/            # Streamlit UI

├── data/                # Your uploaded documents

├── docker-compose.yml   # Run everything with Docker

└── requirements.txt