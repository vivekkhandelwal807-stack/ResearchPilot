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

def reasoner_agent(state: AgentState) -> AgentState:
    """
    Agent 3 - Reasoner + Citation Agent
    Reads retrieved chunks → reasons over them → generates answer with citations
    """
    print("[Reasoner] Generating answer with citations...")

    llm = get_llm()
    query = state["refined_query"] or state["query"]
    docs = state["retrieved_docs"]
    chat_history = state.get("chat_history", [])

    # Format retrieved chunks with source numbers
    context = ""
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", f"Document {i+1}")
        context += f"[Source {i+1}] ({source}):\n{doc.page_content}\n\n"

    # Build conversation history
    history_text = ""
    if chat_history:
        history_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in chat_history[-4:]
        ])

    prompt = f"""You are a research assistant. Answer the question using ONLY the provided context.
Always cite your sources using [Source N] notation.

Previous conversation:
{history_text if history_text else "No previous conversation."}

Context:
{context}

Question: {query}

Instructions:
- Answer clearly and thoroughly
- Cite every fact with [Source N]
- If context doesn't contain the answer, say "I don't have enough information in the provided documents."
- Do not make up information

Answer:"""

    response = llm.invoke(prompt)
    answer = response.content.strip()

    print(f"[Reasoner] ✅ Answer generated")
    return {**state, "final_answer": answer}