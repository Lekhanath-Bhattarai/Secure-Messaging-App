import sqlite3
import hashlib
import os

DB_PATH = "data/users.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_user_db():
    # Create users database and table if not exist
    if not os.path.exists("data"):
        os.mkdir("data")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            public_key TEXT,
            private_key TEXT
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    init_user_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if user exists
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        raise Exception("Username already exists.")
    # Hash the password and insert user
    pwd_hash = hash_password(password)
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, pwd_hash))
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    init_user_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return False
    stored_hash = row[0]
    return stored_hash == hash_password(password)

def get_keys(username):
    init_user_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT public_key, private_key FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row  # (public_key, private_key)
    else:
        raise Exception("User not found.")
