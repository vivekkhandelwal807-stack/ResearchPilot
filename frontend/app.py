import streamlit as st
import requests
import json
from datetime import datetime

# ---- Config ----
API_BASE = "http://localhost:8000/api"

st.set_page_config(
    page_title="RAG Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Custom CSS ----
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .user-message {
        background: #E3F2FD;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #1E88E5;
    }
    .assistant-message {
        background: #F3E5F5;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #8E24AA;
    }
    .source-badge {
        background: #E8F5E9;
        color: #2E7D32;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        margin: 2px;
        display: inline-block;
    }
    .refined-query {
        background: #FFF8E1;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.8rem;
        color: #F57F17;
        margin: 4px 0;
    }
    .status-ok {
        color: #2E7D32;
        font-weight: 600;
    }
    .status-error {
        color: #C62828;
        font-weight: 600;
    }
    .timestamp {
        font-size: 0.7rem;
        color: #999;
        margin-top: 4px;
    }
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


# ---- Helper Functions ----

def check_api_health():
    try:
        r = requests.get(f"{API_BASE.replace('/api', '')}/health", timeout=3)
        return r.status_code == 200
    except:
        return False


def upload_document(file, session_id):
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        r = requests.post(f"{API_BASE}/upload", files=files, timeout=60)
        if r.status_code == 200:
            return True, r.json()
        return False, r.json()
    except Exception as e:
        return False, {"detail": str(e)}


def query_document(query, session_id):
    try:
        payload = {"query": query, "session_id": session_id}
        r = requests.post(f"{API_BASE}/query", json=payload, timeout=60)
        if r.status_code == 200:
            return True, r.json()
        return False, r.json()
    except Exception as e:
        return False, {"detail": str(e)}


def clear_session(session_id):
    try:
        r = requests.delete(f"{API_BASE}/sessions/{session_id}", timeout=10)
        return r.status_code == 200
    except:
        return False


def download_chat_history(messages):
    lines = []
    lines.append("RAG Research Assistant - Chat History")
    lines.append("=" * 40)
    for msg in messages:
        role = "You" if msg["role"] == "user" else "Assistant"
        time = msg.get("timestamp", "")
        lines.append(f"\n[{time}] {role}:")
        lines.append(msg["content"])
        if msg.get("sources"):
            lines.append(f"Sources: {', '.join(msg['sources'])}")
        if msg.get("refined_query"):
            lines.append(f"Refined Query: {msg['refined_query']}")
    return "\n".join(lines)


# ---- Session State Init ----
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "default"

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "api_healthy" not in st.session_state:
    st.session_state.api_healthy = False


# ---- Sidebar ----
with st.sidebar:
    st.markdown("## 🔬 RAG Assistant")
    st.markdown("---")

    # API Status
    api_ok = check_api_health()
    if api_ok:
        st.markdown('<p class="status-ok">🟢 API Connected</p>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-error">🔴 API Offline</p>',
                    unsafe_allow_html=True)
        st.warning("Start the FastAPI server first:\n`uvicorn app.main:app --reload`")

    st.markdown("---")

    # Session Management
    st.markdown("### 🔑 Session")
    session_input = st.text_input(
        "Session ID",
        value=st.session_state.session_id,
        help="Use same ID to continue a conversation"
    )
    if session_input != st.session_state.session_id:
        st.session_state.session_id = session_input
        st.session_state.messages = []
        st.rerun()

    if st.button("🗑️ Clear Session"):
        cleared = clear_session(st.session_state.session_id)
        st.session_state.messages = []
        if cleared:
            st.success("Session cleared!")
        else:
            st.warning("Could not clear server session, cleared local chat.")
        st.rerun()

    st.markdown("---")

    # Document Upload
    st.markdown("### 📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt"],
        help="Supported: PDF, TXT"
    )

    if uploaded_file:
        if st.button("📤 Ingest Document"):
            with st.spinner("Processing document..."):
                success, result = upload_document(
                    uploaded_file,
                    st.session_state.session_id
                )
            if success:
                st.success(f"✅ {result['message']}")
                if uploaded_file.name not in st.session_state.uploaded_files:
                    st.session_state.uploaded_files.append(uploaded_file.name)
            else:
                st.error(f"❌ {result.get('detail', 'Upload failed')}")

    # Uploaded files list
    if st.session_state.uploaded_files:
        st.markdown("### 📚 Ingested Documents")
        for fname in st.session_state.uploaded_files:
            st.markdown(f"- 📄 `{fname}`")

    st.markdown("---")

    # Download Chat
    if st.session_state.messages:
        chat_text = download_chat_history(st.session_state.messages)
        st.download_button(
            label="💾 Download Chat History",
            data=chat_text,
            file_name=f"chat_{st.session_state.session_id}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )

    st.markdown("---")
    st.markdown("**Built with:**")
    st.markdown("🔗 LangGraph · LangChain · Groq · ChromaDB · FastAPI")


# ---- Main Area ----
st.markdown('<p class="main-header">🔬 RAG Research Assistant</p>',
            unsafe_allow_html=True)
st.markdown('<p class="sub-header">Multi-Agent AI for intelligent document analysis and Q&A</p>',
            unsafe_allow_html=True)

# Welcome screen
if not st.session_state.messages:
    st.info("""
    👋 **Welcome! Here's how to get started:**
    
    1. 📄 **Upload a document** (PDF or TXT) from the sidebar
    2. 📤 **Click Ingest Document** to process it
    3. 💬 **Ask questions** about your document below
    4. 📚 **View sources** cited in each answer
    """)

# Chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <strong>You:</strong> {msg['content']}
            <div class="timestamp">{msg.get('timestamp', '')}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <strong>🤖 Assistant:</strong><br>{msg['content']}
        </div>
        """, unsafe_allow_html=True)

        # Show refined query
        if msg.get("refined_query"):
            st.markdown(f"""
            <div class="refined-query">
                🔍 <strong>Refined Query:</strong> {msg['refined_query']}
            </div>
            """, unsafe_allow_html=True)

        # Show sources
        if msg.get("sources"):
            st.markdown("**📚 Sources:**")
            for src in set(msg["sources"]):
                st.markdown(f'<span class="source-badge">📄 {src}</span>',
                            unsafe_allow_html=True)

        st.markdown(f'<div class="timestamp">{msg.get("timestamp", "")}</div>',
                    unsafe_allow_html=True)

    st.markdown("")


# Chat input
st.markdown("---")
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.chat_input("Ask a question about your document...")

if user_input:
    if not api_ok:
        st.error("❌ API is offline. Please start the FastAPI server first.")
    else:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

        # Query API
        with st.spinner("🤔 Agents are thinking..."):
            success, result = query_document(
                user_input,
                st.session_state.session_id
            )

        if success:
            st.session_state.messages.append({
                "role": "assistant",
                "content": result["answer"],
                "refined_query": result.get("refined_query", ""),
                "sources": result.get("sources", []),
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"❌ Error: {result.get('detail', 'Something went wrong')}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

        st.rerun()