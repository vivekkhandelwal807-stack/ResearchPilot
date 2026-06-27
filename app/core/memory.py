from typing import List


def update_memory(
    chat_history: List[dict],
    query: str,
    answer: str,
    max_turns: int = 10
) -> List[dict]:
    """
    Adds latest Q&A to chat history.
    Keeps only last max_turns to avoid context overflow.
    """
    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": answer})

    # Keep only last max_turns * 2 messages (each turn = 1 user + 1 assistant)
    if len(chat_history) > max_turns * 2:
        chat_history = chat_history[-(max_turns * 2):]

    return chat_history


def format_history_for_display(chat_history: List[dict]) -> str:
    """
    Formats chat history for readable display.
    """
    if not chat_history:
        return "No conversation history yet."

    formatted = []
    for msg in chat_history:
        role = "You" if msg["role"] == "user" else "Assistant"
        formatted.append(f"{role}: {msg['content']}")

    return "\n".join(formatted)