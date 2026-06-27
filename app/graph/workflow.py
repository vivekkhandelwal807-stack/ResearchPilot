from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.agents.planner import planner_agent
from app.agents.retriever import retriever_agent
from app.agents.reasoner import reasoner_agent
from app.core.memory import update_memory


def build_graph():
    """
    Builds the LangGraph multi-agent workflow.

    Flow:
    planner → retriever → reasoner → END
    """
    graph = StateGraph(AgentState)

    # Add agent nodes
    graph.add_node("planner", planner_agent)
    graph.add_node("retriever", retriever_agent)
    graph.add_node("reasoner", reasoner_agent)

    # Define edges (flow between agents)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "retriever")
    graph.add_edge("retriever", "reasoner")
    graph.add_edge("reasoner", END)

    return graph.compile()


def run_query(query: str, chat_history: list = []) -> dict:
    """
    Run a query through the full multi-agent pipeline.
    Returns answer + updated chat history.
    """
    graph = build_graph()

    # Initial state
    initial_state: AgentState = {
        "query": query,
        "refined_query": "",
        "retrieved_docs": [],
        "final_answer": "",
        "chat_history": chat_history,
        "document_name": None
    }

    print(f"\n{'='*50}")
    print(f"Running query: '{query}'")
    print(f"{'='*50}")

    # Run the graph
    final_state = graph.invoke(initial_state)

    # Update memory
    updated_history = update_memory(
        chat_history=chat_history,
        query=query,
        answer=final_state["final_answer"]
    )

    return {
        "query": query,
        "refined_query": final_state["refined_query"],
        "answer": final_state["final_answer"],
        "chat_history": updated_history,
        "sources": [
            doc.metadata.get("source", "Unknown")
            for doc in final_state["retrieved_docs"]
        ]
    }