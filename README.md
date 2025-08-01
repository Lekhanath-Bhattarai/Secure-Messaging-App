# Secure Messaging Application

This is a Python-based secure messaging application with end-to-end encryption using RSA public-key cryptography. The app features a simple GUI built with Tkinter, allowing users to register, login, and exchange encrypted messages locally.

---

## Features

- User registration with RSA key pair generation
- Password hashing for secure authentication
- End-to-end encryption of messages using recipients' public keys
- Local SQLite database for user and message storage
- Simple GUI interface for chatting

---


# Usage

Register a new user with a username and password.

Login with registered credentials.

Send encrypted messages to other registered users.

Messages are stored encrypted and decrypted only for the recipient.

## Setup

1. Clone the repository:
   ```bash
   git clone 
   cd secure_messaging
   
2. Create and activate a Python virtual environment:   
	python3 -m venv venv
	source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies:
	pip install -r requirements.txt
	
4. Initialibe database:
	python -c "from core.init_db import init_db; init_db()"

5. Run the Application
	PYTHONPATH=. python3 gui/main_gui.py
	
