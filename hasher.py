from cryptography.fernet import Fernet
import base64
import hashlib


# Function to generate a key from the master password
def generate_key(master_password: str):
    # Hash the master password to generate a key
    password_bytes = master_password.encode()
    # Use SHA-256 to hash the password and get a 32-byte key
    key = base64.urlsafe_b64encode(hashlib.sha256(password_bytes).digest())
    return key


# Function to encrypt the password
def encrypt_password(user_password: str, master_password: str):
    key = generate_key(master_password)
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(user_password.encode())
    return encrypted_password


# Function to decrypt the password
def decrypt_password(encrypted_password: str, master_password: str):
    key = generate_key(master_password)
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password
