import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the encryption key from the .env file
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY').encode()

# Initialize the Fernet class with the encryption key
cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt_data(plain_text: str) -> str:
    """
    Encrypts the provided plain text using the encryption key.
    """
    encrypted_text = cipher_suite.encrypt(plain_text.encode())
    return encrypted_text.decode()  # Return as string for storage in DB or API calls

def decrypt_data(encrypted_text: str) -> str:
    """
    Decrypts the provided encrypted text using the encryption key.
    """
    decrypted_text = cipher_suite.decrypt(encrypted_text.encode())
    return decrypted_text.decode() 
