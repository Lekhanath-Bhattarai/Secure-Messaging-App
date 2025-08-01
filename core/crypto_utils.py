from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def encrypt_with_public_key(public_key_pem, message):
    recipient_key = RSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(recipient_key)
    encrypted_message = cipher.encrypt(message.encode())
    return base64.b64encode(encrypted_message).decode()

def decrypt_with_private_key(private_key_pem, encrypted_message_b64):
    private_key = RSA.import_key(private_key_pem)
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_message = base64.b64decode(encrypted_message_b64)
    return cipher.decrypt(encrypted_message).decode()
