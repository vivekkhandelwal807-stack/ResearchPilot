from typing import TypedDict, List, Optional
from langchain_core.documents import Document


class AgentState(TypedDict):
    """
    Shared state passed between all agents in the graph.
    Every agent reads from and writes to this state.
    """
    query: str                          # original user query
    refined_query: str                  # planner's improved query
    retrieved_docs: List[Document]      # chunks from ChromaDB
    final_answer: str                   # reasoner's final answer
    chat_history: List[dict]            # conversational memory
    document_name: Optional[str]        # which doc was uploaded