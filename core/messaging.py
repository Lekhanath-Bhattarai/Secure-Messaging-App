import os
import sqlite3
from datetime import datetime, timezone

def init_db():
    conn = sqlite3.connect("data/messages.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def store_message(sender, receiver, message):
    conn = sqlite3.connect("data/messages.db")
    cursor = conn.cursor()
    timestamp = datetime.now(timezone.utc).isoformat()
    cursor.execute(
        "INSERT INTO messages (sender, receiver, message, timestamp) VALUES (?, ?, ?, ?)",
        (sender, receiver, message, timestamp)
    )
    conn.commit()
    conn.close()

def get_messages_for_user(username):
    conn = sqlite3.connect("data/messages.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sender, message, timestamp FROM messages WHERE receiver = ? ORDER BY id ASC",
        (username,)
    )
    messages = cursor.fetchall()
    conn.close()
    return messages
