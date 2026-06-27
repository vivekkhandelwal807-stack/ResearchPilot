from app.graph.state import AgentState
from app.core.vectorstore import get_retriever


def retriever_agent(state: AgentState) -> AgentState:
    """
    Agent 2 - Retriever Agent
    Takes refined query from planner → searches ChromaDB → returns relevant chunks
    """
    print("[Retriever] Searching vector store...")

    refined_query = state.get("refined_query") or state["query"]

    retriever = get_retriever(k=4)
    docs = retriever.invoke(refined_query)

    print(f"[Retriever] ✅ Found {len(docs)} relevant chunks")
    for i, doc in enumerate(docs):
        preview = doc.page_content[:80].replace("\n", " ")
        print(f"  Chunk {i+1}: {preview}...")

    return {**state, "retrieved_docs": docs}