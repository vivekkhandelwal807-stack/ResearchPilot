from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=r"D:\vivek-final\.env", override=True)
print("Key loaded:", os.getenv("GOOGLE_API_KEY"))  # confirm it loads

from app.graph.state import AgentState
from app.agents.planner import planner_agent
from app.agents.retriever import retriever_agent
from app.core.pipeline import build_pipeline

# First make sure document is ingested
build_pipeline("data/sample.txt")

# Simulate initial state
state: AgentState = {
    "query": "wat is rag n how it works?",
    "refined_query": "",
    "retrieved_docs": [],
    "final_answer": "",
    "chat_history": [],
    "document_name": "sample.txt"
}

# Agent 1 - Planner
state = planner_agent(state)

# Agent 2 - Retriever
state = retriever_agent(state)

print(f"\n--- Retrieved {len(state['retrieved_docs'])} Chunks ---")
for i, doc in enumerate(state["retrieved_docs"]):
    print(f"\nChunk {i+1}:")
    print(doc.page_content)