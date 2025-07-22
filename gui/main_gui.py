import tkinter as tk
from tkinter import messagebox, scrolledtext
from core.user_management import register_user, get_keys
from core.messaging import store_message, get_messages_for_user

current_user = None

def register():
    username = entry_username.get()
    if username:
        register_user(username)
        messagebox.showinfo("Success", f"User '{username}' registered!")
    else:
        messagebox.showerror("Error", "Username required.")

def login():
    global current_user
    username = entry_username.get()
    try:
        get_keys(username)
        current_user = username
        open_chat_window()
    except:
        messagebox.showerror("Error", "User not found. Please register.")

def open_chat_window():
    login_window.destroy()

    chat = tk.Tk()
    chat.title(f"Secure Chat - {current_user}")

    tk.Label(chat, text="To:").grid(row=0, column=0)
    entry_to = tk.Entry(chat)
    entry_to.grid(row=0, column=1)

    tk.Label(chat, text="Message:").grid(row=1, column=0)
    entry_msg = tk.Entry(chat, width=50)
    entry_msg.grid(row=1, column=1, padx=5, pady=5)

    def send_msg():
        to_user = entry_to.get()
        msg = entry_msg.get()
        if to_user and msg:
            store_message(current_user, to_user, msg)
            entry_msg.delete(0, tk.END)
            update_messages()
        else:
            messagebox.showerror("Error", "Both fields required.")

    def update_messages():
        chat_log.delete(1.0, tk.END)
        messages = get_messages_for_user(current_user)
        for sender, msg, ts in messages:
            chat_log.insert(tk.END, f"[{ts}] {sender}: {msg}\n")

    tk.Button(chat, text="Send", command=send_msg).grid(row=1, column=2, padx=5)
    chat_log = scrolledtext.ScrolledText(chat, width=70, height=20)
    chat_log.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

    update_messages()
    chat.mainloop()

# Login/Register window
login_window = tk.Tk()
login_window.title("Secure Messaging - Login/Register")

tk.Label(login_window, text="Username:").grid(row=0, column=0)
entry_username = tk.Entry(login_window)
entry_username.grid(row=0, column=1)

tk.Button(login_window, text="Register", command=register).grid(row=1, column=0, pady=10)
tk.Button(login_window, text="Login", command=login).grid(row=1, column=1)

login_window.mainloop()
