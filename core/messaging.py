import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = "data/messages.db"

def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            recipient TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def store_message(sender, recipient, message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now(timezone.utc).isoformat()
    cursor.execute("INSERT INTO messages (sender, recipient, message, timestamp) VALUES (?, ?, ?, ?)",
                   (sender, recipient, message, timestamp))
    conn.commit()
    conn.close()

def retrieve_messages(recipient):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sender, message, timestamp FROM messages WHERE recipient = ?", (recipient,))
    rows = cursor.fetchall()
    conn.close()
    return rows
