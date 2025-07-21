from core.user_management import register_user, get_keys
from core.crypto_utils import encrypt_message, decrypt_message
from core.messaging import store_message, retrieve_messages

def menu():
    print("\n--- Secure Messaging CLI ---")
    print("1. Register User")
    print("2. Encrypt and Send Message")
    print("3. Read Messages")
    print("4. Exit")
    return input("Choose: ")

def main():
    while True:
        choice = menu()
        if choice == '1':
            username = input("Enter username: ")
            success, msg = register_user(username)
            print(msg)

        elif choice == '2':
            sender = input("Your username: ")
            receiver = input("Recipient username: ")
            message = input("Message to send: ")

            # Get recipient's public key
            try:
                _, receiver_pub = get_keys(receiver)
            except FileNotFoundError:
                print(f"Recipient '{receiver}' not found.")
                continue

            encrypted = encrypt_message(message, receiver_pub)
            # Store the encrypted message as stringified dict
            store_message(sender, receiver, str(encrypted))
            print("Encrypted message sent and stored.")

        elif choice == '3':
            username = input("Enter your username to read messages: ")
            msgs = retrieve_messages(username)
            if not msgs:
                print("No messages found.")
                continue

            # Get user's private key
            try:
                private_key, _ = get_keys(username)
            except FileNotFoundError:
                print(f"User '{username}' not found.")
                continue

            print(f"\nMessages for {username}:")
            for sender, encrypted_str, timestamp in msgs:
                encrypted = eval(encrypted_str)  # convert string back to dict
                try:
                    decrypted = decrypt_message(encrypted, private_key)
                except Exception as e:
                    decrypted = "[Failed to decrypt]"
                print(f"From: {sender} at {timestamp}\nMessage: {decrypted}\n")

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
