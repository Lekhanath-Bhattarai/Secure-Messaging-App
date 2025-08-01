import sqlite3
import hashlib
import os
from Crypto.PublicKey import RSA

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

def get_user_dir(username):
    return os.path.join("data", "users", username)

def get_public_key_path(username):
    return os.path.join(get_user_dir(username), "public.pem")

def get_private_key_path(username):
    return os.path.join(get_user_dir(username), "private.pem")

def register_user(username, password):
    init_user_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if user exists
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        raise Exception("Username already exists.")

    pwd_hash = hash_password(password)

    # Generate RSA key pair
    key = RSA.generate(2048)
    private_key = key.export_key().decode()
    public_key = key.publickey().export_key().decode()

    user_dir = get_user_dir(username)
    os.makedirs(user_dir, exist_ok=True)

    # Save keys as files
    with open(get_private_key_path(username), 'w') as f:
        f.write(private_key)
    with open(get_public_key_path(username), 'w') as f:
        f.write(public_key)

    # Save user info and keys in DB
    cursor.execute(
        "INSERT INTO users (username, password_hash, public_key, private_key) VALUES (?, ?, ?, ?)",
        (username, pwd_hash, public_key, private_key)
    )
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

def user_exists(username):
    conn = sqlite3.connect("data/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
