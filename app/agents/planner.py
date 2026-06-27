import os
 
from app.graph.state import AgentState
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY, LLM_MODEL

def get_llm():
    return ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.3
    )
    


def planner_agent(state: AgentState) -> AgentState:
    """
    Agent 1 - Query Planner
    Takes the raw user query and refines it for better retrieval.
    """
    print("[Planner] Analyzing and refining query...")

    llm = get_llm()
    query = state["query"]
    chat_history = state.get("chat_history", [])

    history_text = ""
    if chat_history:
        history_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in chat_history[-4:]
        ])

    prompt = f"""You are a query planning expert. Your job is to refine and improve user queries for better document retrieval.

Previous conversation:
{history_text if history_text else "No previous conversation."}

Original query: {query}

Rewrite this query to be more specific and retrieval-friendly.
- Fix typos
- Expand abbreviations  
- Make it more descriptive
- Keep it as ONE clear question

Return ONLY the refined query, nothing else."""

    response = llm.invoke(prompt)
    refined = response.content.strip()

    print(f"[Planner] Original: '{query}'")
    print(f"[Planner] Refined:  '{refined}'")

    return {**state, "refined_query": refined}