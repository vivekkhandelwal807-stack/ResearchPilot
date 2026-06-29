import sqlite3
import json
import os
from datetime import datetime
from typing import List

DB_PATH = "sessions.db"


def get_connection():
    """Get SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Create tables if they don't exist.
    Called once when app starts.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            messages TEXT NOT NULL DEFAULT '[]',
            document_name TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uploaded_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            session_id TEXT,
            uploaded_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("[Database] ✅ SQLite initialized")


def save_session(session_id: str, messages: List[dict], document_name: str = None):
    """
    Save or update a chat session.
    """
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO chat_sessions (session_id, messages, document_name, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(session_id) DO UPDATE SET
            messages = excluded.messages,
            document_name = excluded.document_name,
            updated_at = excluded.updated_at
    """, (session_id, json.dumps(messages), document_name, now, now))

    conn.commit()
    conn.close()


def load_session(session_id: str) -> List[dict]:
    """
    Load chat history for a session.
    Returns empty list if session doesn't exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT messages FROM chat_sessions WHERE session_id = ?",
        (session_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return json.loads(row["messages"])
    return []


def delete_session(session_id: str):
    """
    Delete a chat session.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM chat_sessions WHERE session_id = ?",
        (session_id,)
    )
    conn.commit()
    conn.close()


def save_document(filename: str, file_path: str, session_id: str = None):
    """
    Save uploaded document record.
    """
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO uploaded_documents (filename, file_path, session_id, uploaded_at)
        VALUES (?, ?, ?, ?)
    """, (filename, file_path, session_id, now))

    conn.commit()
    conn.close()


def get_all_documents() -> List[dict]:
    """
    Get all uploaded documents.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM uploaded_documents ORDER BY uploaded_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_all_sessions() -> List[dict]:
    """
    Get all sessions summary.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT session_id, document_name, created_at, updated_at
        FROM chat_sessions
        ORDER BY updated_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]