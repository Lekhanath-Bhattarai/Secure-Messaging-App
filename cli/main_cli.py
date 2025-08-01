import sys
import os
from datetime import datetime

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.init_db import init_db
from core.user_management import user_exists, init_user_db, register_user, authenticate_user
from core.messaging import store_message, get_messages_for_user

# Initialize databases
init_db()
init_user_db()

current_user = None

def register():
    username = input("Enter a username to register: ").strip()
    password = input("Enter a password: ")
    if username and password:
        try:
            register_user(username, password)
            print(f"✅ User '{username}' registered successfully!\n")
        except Exception as e:
            print(f"❌ Registration failed: {str(e)}\n")
    else:
        print("❌ Username and password are required.\n")

def login():
    global current_user
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ")
    if username and password:
        if authenticate_user(username, password):
            current_user = username
            print(f"✅ Welcome, {username}!\n")
            open_chat()
        else:
            print("❌ Invalid username or password.\n")
    else:
        print("❌ Username and password are required.\n")

def open_chat():
    while True:
        print("\n--- Secure Messaging CLI ---")
        print("1. View messages")
        print("2. Send message")
        print("3. Logout")

        choice = input("Select an option: ").strip()

        if choice == '1':
            view_messages()
        elif choice == '2':
            send_message()
        elif choice == '3':
            print("🔒 Logging out...\n")
            break
        else:
            print("❌ Invalid option. Try again.")

def view_messages():
    print("\n📥 Your messages:\n")
    messages = get_messages_for_user(current_user)
    if messages:
        for sender, msg, ts in messages:
            print(f"[{ts}] {sender}: {msg}")
    else:
        print("No messages found.")

def send_message():
    to_user = input("Send to: ").strip()
    msg = input("Message: ").strip()

    if not to_user or not msg:
        print("❌ Recipient and message are required.\n")
        return

    if not user_exists(to_user):
        print(f"❌ User '{to_user}' does not exist.\n")
        return

    try:
        store_message(current_user, to_user, msg)
        print("✅ Message sent successfully.\n")
    except FileNotFoundError as e:
        print(f"❌ Error: {str(e)}\n")

def main():
    while True:
        print("=== Secure Messaging CLI ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Select an option: ").strip()

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("👋 Exiting. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
