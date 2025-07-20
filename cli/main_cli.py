from core.user_management import register_user, get_keys
from core.crypto_utils import encrypt_message, decrypt_message

def menu():
    print("1. Register User")
    print("2. Encrypt Message")
    print("3. Decrypt Message")
    print("4. Exit")
    return input("Choose: ")

while True:
    choice = menu()
    if choice == '1':
        username = input("Enter username: ")
        success, msg = register_user(username)
        print(msg)
    elif choice == '2':
        sender = input("Sender username: ")
        receiver = input("Receiver username: ")
        message = input("Message to encrypt: ")

        _, receiver_pub = get_keys(receiver)
        encrypted = encrypt_message(message, receiver_pub)
        print("Encrypted message:", encrypted)
    elif choice == '3':
        username = input("Enter your username: ")
        private_key, _ = get_keys(username)
        encrypted = eval(input("Paste encrypted message dict: "))
        decrypted = decrypt_message(encrypted, private_key)
        print("Decrypted message:", decrypted)
    elif choice == '4':
        break
    else:
        print("Invalid choice.")
