import os
import sqlite3
from core.messaging import init_db, store_message, retrieve_messages

def setup_module(module):
    if os.path.exists("data/messages.db"):
        os.remove("data/messages.db")
    init_db()

def test_store_and_retrieve_message():
    store_message("Alice", "Bob", "Hello Bob!")
    messages = retrieve_messages("Bob")
    assert len(messages) == 1
    assert messages[0][0] == "Alice"
    assert messages[0][1] == "Hello Bob!"
