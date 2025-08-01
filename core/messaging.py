import sqlite3
import os
from core.crypto_utils import encrypt_with_public_key, decrypt_with_private_key
from core.user_management import get_public_key_path, get_private_key_path

DB_PATH = "data/messages.db"

def store_message(sender, receiver, message):
    pub_key_path = get_public_key_path(receiver)
    if not os.path.exists(pub_key_path):
        raise FileNotFoundError(f"Public key for {receiver} not found.")

    with open(pub_key_path, "rb") as f:
        pub_key_pem = f.read()

    encrypted_msg = encrypt_with_public_key(pub_key_pem, message)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (sender, receiver, message)
        VALUES (?, ?, ?)
    """, (sender, receiver, encrypted_msg))
    conn.commit()
    conn.close()

def get_messages_for_user(username):
    priv_key_path = get_private_key_path(username)
    if not os.path.exists(priv_key_path):
        return []

    with open(priv_key_path, "rb") as f:
        priv_key_pem = f.read()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender, message, timestamp FROM messages
        WHERE receiver = ?
        ORDER BY id ASC
    """, (username,))
    rows = cursor.fetchall()
    conn.close()

    decrypted = []
    for sender, enc_msg, ts in rows:
        try:
            msg = decrypt_with_private_key(priv_key_pem, enc_msg)
        except Exception:
            msg = "[Decryption Failed]"
        decrypted.append((sender, msg, ts))
    return decrypted
