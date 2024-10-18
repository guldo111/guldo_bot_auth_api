import secrets
from cryptography.fernet import Fernet
from core.config import settings
from typing import Any

cipher_suite = Fernet(settings.encryption_key.encode())

def encrypt_data(plain_text: str) -> str:
    """
    Encrypts the provided plain text.

    Args:
        plain_text (str): The text to encrypt.

    Returns:
        str: The encrypted text.
    """
    return cipher_suite.encrypt(plain_text.encode()).decode()

def decrypt_data(encrypted_text: str) -> str:
    """
    Decrypts the provided encrypted text.

    Args:
        encrypted_text (str): The text to decrypt.

    Returns:
        str: The decrypted plain text.
    """
    return cipher_suite.decrypt(encrypted_text.encode()).decode()

def generate_api_key(length: int = 32) -> str:
    """
    Generates a secure API key.

    Args:
        length (int): The length of the API key. Default is 32 characters.

    Returns:
        str: A securely generated API key.
    """
    return secrets.token_urlsafe(length)