from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_message(key, message):
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(key, encrypted_message):
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

if __name__ == "__main__":
    key = generate_key()
    print(f"Encryption Key: {key.decode()}")

    message = input("Enter a message to encrypt: ")
    encrypted_message = encrypt_message(key, message)
    print(f"Encrypted Message: {encrypted_message.decode()}")

    decrypted_message = decrypt_message(key, encrypted_message)
    print(f"Decrypted Message: {decrypted_message}")
