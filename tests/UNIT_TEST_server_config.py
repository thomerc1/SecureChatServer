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
Server Config Unit Test
=======================================================
"""

import sys
import os
import unittest

# Append the source dirs to the Python Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import sources to test
from config.server_config import ServerConfig

class TestServerConfig(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment. Remove existing config file if it exists.
        """
        self.config_file = "config.json"
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        self.config = ServerConfig()

    def test_initial_values(self):
        """
        Test the initial values of ssh_enabled and encryption_enabled.
        """
        self.assertFalse(self.config.ssh_enabled)
        self.assertFalse(self.config.encryption_enabled)

    def test_set_and_get_ssh_enabled(self):
        """
        Test setting and getting the ssh_enabled property.
        """
        self.config.ssh_enabled = True
        self.assertTrue(self.config.ssh_enabled)

    def test_set_and_get_encryption_enabled(self):
        """
        Test setting and getting the encryption_enabled property.
        """
        self.config.encryption_enabled = True
        self.assertTrue(self.config.encryption_enabled)

    def test_save_and_load_config(self):
        """
        Test saving to and loading from the config file.
        """
        self.config.ssh_enabled = True
        self.config.encryption_enabled = True
        self.config.save_config()

        # Create a new instance to test loading from file
        new_config = ServerConfig()
        self.assertTrue(new_config.ssh_enabled)
        self.assertTrue(new_config.encryption_enabled)

    def tearDown(self):
        """
        Clean up after tests. Remove the created config file.
        """
        if os.path.exists(self.config_file):
            os.remove(self.config_file)


if __name__ == '__main__':
    unittest.main(verbosity=2)
