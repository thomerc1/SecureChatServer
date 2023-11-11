"""
Course Name: CMSC495 7384
Project: CMSC495 Secure Chat Server
Group: A
Author: Eric Thomas
Date: Nov 23'
Platform: Debian Linux
Dependency: Python 3.10 +
=======================================================
Description:
Encryption Tools Module

This module provides functions for encrypting and decrypting data using a Fernet cipher
derived from a user-provided password. It also includes a function for generating
a SHA-256 hash from a password.
=======================================================
Reference(s):
Function development referenced Python Cryptography documentation: 
https://cryptography.io/en/latest/fernet/
=======================================================
"""

import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import traceback
import base64


def encrypt_data_with_password(data: bytes, password: str) -> bytes:
    """
    Encrypts data using a Fernet cipher derived from a password.

    Args:
        data (bytes): The data to be encrypted.
        password (str): The password used to derive the cipher.

    Returns:
        bytes: The encrypted data.
    """
    cipher = _fernet_cipher_from_password(password)
    encrypted_data = cipher.encrypt(data)
    return encrypted_data


def decrypt_data_with_password(encrypted_data: bytes, password: str) -> bytes:
    """
    Decrypts data using a Fernet cipher derived from a password.

    Args:
        encrypted_data (bytes): The encrypted data.
        password (str): The password used to derive the cipher.

    Returns:
        bytes: The decrypted data.
    """
    cipher = _fernet_cipher_from_password(password)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data


def _fernet_cipher_from_password(password: str) -> Fernet:
    """
    Internal function to derive a Fernet cipher from a password.

    Args:
        password (str): The password used to derive the cipher.

    Returns:
        Fernet: The derived Fernet cipher.
    """
    cipher = None

    try:
        # Key derivation function (KDF) to derive a fixed-size key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'',
            iterations=100000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))

        # Initialize the Fernet cipher with the derived key
        cipher = Fernet(key)
    except:
        traceback.print_exc()

    return cipher


def get_password_hash(password: str) -> str:
    """
    Creates and returns a SHA-256 hash from a password.

    Args:
        password (str): The password used to generate the hash.

    Returns:
        str: The SHA-256 hash as a hex string.
    """
    # Generate and return SHA-256 hash of the password
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


if __name__ == "__main__":
    # Example usage:
    try:
        # Never store real password in our application (only the hash)
        stored_password = "test_password"
        stored_hash = get_password_hash(stored_password)

        print(f"The correct password is:\n{stored_password}")
        print(f"The stored hash is:\n{stored_hash}")
        print()

        # User enters password
        test_password = input("Enter the password for encryption and decryption: ")
        test_hash = get_password_hash(test_password.strip())

        if (test_hash == stored_hash):
            print("User entered the correct password")

            # Get a test string
            user_input = input("Enter a string to test: ")

            # Show user what they entered
            print(f"You entered: {user_input}")

            # Encrypt user input
            encrypted_user_input = encrypt_data_with_password(user_input.encode('utf-8'), test_password)

            # Decrypt user input
            decrypted_user_input = decrypt_data_with_password(encrypted_user_input, test_password)

            # Convert from binary UTF-8 to ASCII
            decrypted_user_input = decrypted_user_input.decode('utf-8')

            # Show user the decrypted data
            print(f"The decrypted data is: {decrypted_user_input}")

            # Verify that the original user data and the decrypted data match
            if user_input == decrypted_user_input:
                print("Successfully encrypted and decrypted the data with a password")
            else:
                print("Error encrypting and decrypting the user data")
        else:
            print("Incorrect password entered")

    except:
        traceback.print_exc()
