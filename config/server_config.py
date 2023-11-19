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
Server Configuration Module

This module defines a server configuration class used by various functions in the Secure Chat Server project.
The `ServerConfig` class encapsulates configuration settings such as SSH and encryption settings.
=======================================================
"""

import json
import os
import unittest
from typing import NoReturn


class ServerConfig:
    """
    Server Configuration used by the application.
    """

    __MAX_USERNAME_LENGTH = 50
    __MAX_MESSAGE_LENGTH = 255
    DEFAULT_SSH_ENABLED = False
    DEFAULT_ENC_ENABLED = False
    DEFAULT_PASSWORD_HASH = 'c5b29c08b4df41903c2df399298a4112bc6a67619d1a3ad901e0377d3fa1c18e'
    PASSWORD_HASH_KEY = 'password_hash'
    SSH_ENABLED_KEY = 'ssh_enabled'
    ENCRYPTION_ENABLED_KEY = 'encryption_enabled'

    def __init__(self) -> NoReturn:
        """
        Initialize the ServerConfig instance and load the configuration from a JSON file.

        Args:
            None

        Returns:
            NoReturn
        """
        self.config_filename = os.path.join(os.path.dirname(__file__), "config.json")
        self.version_filename = os.path.join(os.path.dirname(__file__), "version.txt")
        self._version = self._load_version()
        self.config = {}
        self.load_config()

    def _load_version(self) -> str:
        """
        Read the version from and return the first 7 characters (expected to be a git hash)

        Returns:
            str: The version string (first 7 characters) if file exists, else "none"
        """
        try:
            with open(self.version_filename, "r") as version_file:
                return version_file.read().strip()[:7]
        except Exception:
            return "none"

    def load_config(self) -> NoReturn:
        """
        Load configuration from the 'config.json' file. If the file doesn't exist, it creates one with default values.

        Args:
            None

        Returns:
            NoReturn
        """
        try:
            with open(self.config_filename, "r") as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            # If no config established, set default values and save the config
            self.config = {
                self.PASSWORD_HASH_KEY: self.DEFAULT_PASSWORD_HASH,
                self.SSH_ENABLED_KEY: self.DEFAULT_SSH_ENABLED,
                self.ENCRYPTION_ENABLED_KEY: self.DEFAULT_ENC_ENABLED
            }
            self.save_config()

    @property
    def version(self) -> str:
        """
        Get the software suite version.

        Args:
            None

        Returns:
            str: The version.
        """
        return self._version

    @property
    def password_hash(self) -> str:
        """
        Get the current password hash.

        Args:
            None

        Returns:
            str: The password hash.
        """
        return self.config.get(self.PASSWORD_HASH_KEY, self.DEFAULT_PASSWORD_HASH)

    @password_hash.setter
    def password_hash(self, new_hash: str) -> NoReturn:
        """
        Set the password hash and save it to the configuration file.

        Args:
            new_hash (str): New password hash.

        Returns:
            NoReturn
        """
        self.config[self.PASSWORD_HASH_KEY] = new_hash
        self.save_config()

    def save_config(self) -> NoReturn:
        """
        Save the current configuration to the 'config.json' file.

        Args:
            None

        Returns:
            NoReturn
        """
        with open(self.config_filename, "w") as config_file:
            json.dump(self.config, config_file, indent=4)

    @property
    def ssh_enabled(self) -> bool:
        """
        Get the current SSH enabled status.

        Args:
            None

        Returns:
            bool: Indicates whether SSH is enabled. Default False if config file DNE.
        """
        return self.config.get(self.SSH_ENABLED_KEY, self.DEFAULT_SSH_ENABLED)

    @ssh_enabled.setter
    def ssh_enabled(self, value: bool) -> NoReturn:
        """
        Set the SSH enabled status and save it to the configuration file.

        Args:
            value (bool): New SSH enabled status.

        Returns:
            NoReturn
        """
        self.config[self.SSH_ENABLED_KEY] = value
        self.save_config()

    @property
    def encryption_enabled(self) -> bool:
        """
        Get the current encryption enabled status.

        Args:
            None

        Returns:
            bool: Indicates whether encryption is enabled. Default False if config file DNE.
        """
        return self.config.get(self.ENCRYPTION_ENABLED_KEY, self.DEFAULT_ENC_ENABLED)

    @encryption_enabled.setter
    def encryption_enabled(self, value: bool) -> NoReturn:
        """
        Set the encryption enabled status and save it to the configuration file.

        Args:
            value (bool): New encryption enabled status.

        Returns:
            NoReturn
        """
        self.config[self.ENCRYPTION_ENABLED_KEY] = value
        self.save_config()

    @staticmethod
    def max_username_length() -> int:
        """
        Retrieve the maximum allowed length for usernames.

        Args:
            None

        Returns:
            int: Maximum allowed length for usernames.
        """
        return ServerConfig.__MAX_USERNAME_LENGTH

    @staticmethod
    def max_message_length() -> int:
        """
        Retrieve the maximum allowed length for chat messages.

        Args:
            None

        Returns:
            int: Maximum allowed length for chat messages.
        """
        return ServerConfig.__MAX_MESSAGE_LENGTH

    def print_params(self) -> NoReturn:
        """
        Print the current server configuration parameters.

        Args:
            None

        Returns:
            NoReturn
        """
        print("Current Server Configuration:")
        print(f"SSH Enabled: {self.ssh_enabled}")
        print(f"Encryption Enabled: {self.encryption_enabled}")
        print(f"Max Username Length: {ServerConfig.__MAX_USERNAME_LENGTH}")
        print(f"Max Message Length: {ServerConfig.__MAX_MESSAGE_LENGTH}")
        print(f"Password Hash: {self.password_hash}")


if __name__ == '__main__':
    # Example usage:

    # Create ServerConfig instance
    server_config = ServerConfig()

    # Load Config
    server_config.load_config()

    # Print the default config
    print(f"SSH Enabled: {server_config.ssh_enabled}")
    print(f"Encryption Enabled: {server_config.encryption_enabled}")
    print(f"Max Username Length: {server_config.max_username_length}")
    print(f"Max Message Length: {server_config.max_message_length}")
    print(f"Password hash: {server_config.password_hash}")
    print(f"Version: {server_config.version}")

    # Update the config
    server_config.ssh_enabled = True
    server_config.encryption_enabled = True
    server_config.password_hash = "stuff"

    # Store the updates
    server_config.save_config()

    server_config_2 = ServerConfig()
    server_config_2.load_config()

    # Print the config
    print(f"SSH Enabled: {server_config.ssh_enabled}")
    print(f"Encryption Enabled: {server_config.encryption_enabled}")
    print(f"Max Username Length: {server_config.max_username_length}")
    print(f"Max Message Length: {server_config.max_message_length}")
    print(f"Password hash: {server_config.password_hash}")
    print(f"Version: {server_config.version}")

    # Delete the test config file
    try:
        os.remove(server_config.config_filename)
        print(f"Config file '{server_config.config_filename}' deleted.")
    except OSError as e:
        print(f"Error: {e.strerror}")
