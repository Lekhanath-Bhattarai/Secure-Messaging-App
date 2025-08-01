import tkinter as tk
from tkinter import messagebox, scrolledtext
import sys
import os

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
    username = entry_username.get().strip()
    password = entry_password.get()
    if username and password:
        try:
            register_user(username, password)
            messagebox.showinfo("Success", f"User '{username}' registered!")
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
    else:
        messagebox.showerror("Error", "Username and password required.")

def login():
    global current_user
    username = entry_username.get().strip()
    password = entry_password.get()
    if username and password:
        if authenticate_user(username, password):
            current_user = username
            open_chat_window()
        else:
            messagebox.showerror("Error", "Invalid username or password.")
    else:
        messagebox.showerror("Error", "Username and password required.")

def open_login_window():
    global login_window, entry_username, entry_password

    login_window = tk.Tk()
    login_window.title("Secure Messaging - Login/Register")

    tk.Label(login_window, text="Username:").grid(row=0, column=0)
    entry_username = tk.Entry(login_window)
    entry_username.grid(row=0, column=1)

    tk.Label(login_window, text="Password:").grid(row=1, column=0)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.grid(row=1, column=1)

    tk.Button(login_window, text="Register", command=register).grid(row=2, column=0, pady=10)
    tk.Button(login_window, text="Login", command=login).grid(row=2, column=1)

    login_window.mainloop()

def open_chat_window():
    global login_window
    login_window.destroy()

    chat = tk.Tk()
    chat.title(f"Secure Chat - {current_user}")

    tk.Label(chat, text="To:").grid(row=0, column=0)
    entry_to = tk.Entry(chat)
    entry_to.grid(row=0, column=1)

    tk.Label(chat, text="Message:").grid(row=1, column=0)
    entry_msg = tk.Entry(chat, width=50)
    entry_msg.grid(row=1, column=1, padx=5, pady=5)

    chat_log = scrolledtext.ScrolledText(chat, width=70, height=20)
    chat_log.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

    def update_messages():
        chat_log.delete(1.0, tk.END)
        messages = get_messages_for_user(current_user)
        for sender, msg, ts in messages:
            chat_log.insert(tk.END, f"[{ts}] {sender}: {msg}\n")

    def send_msg():
        to_user = entry_to.get().strip()
        msg = entry_msg.get().strip()

        if not to_user or not msg:
            messagebox.showerror("Error", "Please enter recipient and message.")
            return

        if not user_exists(to_user):
            messagebox.showerror("Error", f"User '{to_user}' does not exist.")
            return

        try:
            store_message(current_user, to_user, msg)
            entry_msg.delete(0, 'end')
            update_messages()
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))

    def logout():
        chat.destroy()
        open_login_window()

    tk.Button(chat, text="Send", command=send_msg).grid(row=1, column=2, padx=5)
    tk.Button(chat, text="Logout", command=logout).grid(row=0, column=3, padx=10)

    update_messages()
    chat.mainloop()

open_login_window()
