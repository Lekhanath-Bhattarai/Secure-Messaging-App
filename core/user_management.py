import os
from core.crypto_utils import generate_rsa_keys

USER_FOLDER = "data/users"

def register_user(username):
    os.makedirs(USER_FOLDER, exist_ok=True)
    user_path = os.path.join(USER_FOLDER, username)
    if os.path.exists(user_path):
        return False, "User already exists."

    os.makedirs(user_path)
    private_key, public_key = generate_rsa_keys()

    with open(os.path.join(user_path, "private.pem"), "wb") as f:
        f.write(private_key)
    with open(os.path.join(user_path, "public.pem"), "wb") as f:
        f.write(public_key)

    return True, "User registered successfully."

def get_keys(username):
    user_path = os.path.join(USER_FOLDER, username)
    with open(os.path.join(user_path, "private.pem"), "rb") as f:
        private = f.read()
    with open(os.path.join(user_path, "public.pem"), "rb") as f:
        public = f.read()
    return private, public
