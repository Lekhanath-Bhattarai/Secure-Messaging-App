from core.crypto_utils import generate_rsa_keys, encrypt_message, decrypt_message

def test_encryption_decryption():
    private_key, public_key = generate_rsa_keys()
    message = "Hello secure world"
    encrypted = encrypt_message(message, public_key)
    decrypted = decrypt_message(encrypted, private_key)
    assert decrypted == message
