"""
=======================================================
Course Name: CMSC495 7384
Project: CMSC495 Secure Chat Server
Group: A
Author: Eric Thomas
Date: Nov 23'
Platform: Debian Linux
Dependency: Python 3.10 +
=======================================================
Description:
Encryption Tools Unit Test
=======================================================
"""

import sys
import os
import unittest

# Append the source dirs to the Python Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import sources to test
# autopep8: off
from utils.encryption_tools import encrypt_data_with_password, decrypt_data_with_password, get_password_hash
# autopep8: on


class TestEncryptionTools(unittest.TestCase):
    def test_password_hash(self):
        """
        Test that the password hashing function returns the correct SHA-256 hash.
        """
        password = "test_password"
        expected_hash = "your_expected_hash_here"  # replace with the actual expected hash
        self.assertEqual(get_password_hash(password), expected_hash)

    def test_encrypt_decrypt(self):
        """
        Test encryption and decryption of data using a password.
        """
        password = "test_password"
        original_data = "This is a test string."

        encrypted_data = encrypt_data_with_password(original_data.encode('utf-8'), password)
        decrypted_data = decrypt_data_with_password(encrypted_data, password).decode('utf-8')

        self.assertEqual(original_data, decrypted_data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
