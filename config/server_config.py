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
Configuration Parameters Module

This module defines a server configuration class used by various functions in the Secure Chat Server project.
The `ServerConfig` class encapsulates configuration settings such as SSH and encryption settings.
=======================================================
"""

import json


class ServerConfig:
    """
    Server Configuration used by the application.

    Attributes:
        ssh_enabled (bool): Indicates whether SSH is enabled.
        encryption_enabled (bool): Indicates whether encryption is enabled.
        MAX_USERNAME_LENGTH (int): Maximum allowed length for usernames.
        MAX_MESSAGE_LENGTH (int): Maximum allowed length for chat messages.
    """

    MAX_USERNAME_LENGTH = 50
    MAX_MESSAGE_LENGTH = 255

    def __init__(self):
        """
        Initialize ConfigurationParams and load configuration from JSON file.
        """
        self.config = {}
        self.load_config()

    def load_config(self):
        """
        Load configuration from the JSON file. If the file doesn't exist, create it with default values.
        """
        try:
            with open("config.json", "r") as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            # Handle the case where the file doesn't exist yet
            self.save_config()

    def save_config(self):
        """
        Save the current configuration to the JSON file.
        """
        with open("config.json", "w") as config_file:
            json.dump(self.config, config_file, indent=4)

    @property
    def ssh_enabled(self):
        """
        bool: Indicates whether SSH is enabled.
        """
        return self.config.get("ssh_enabled", False)

    @ssh_enabled.setter
    def ssh_enabled(self, value):
        """
        Set the SSH enabled status and save it to the configuration file.

        Args:
            value (bool): New SSH enabled status.
        """
        self.config["ssh_enabled"] = value
        self.save_config()

    @property
    def encryption_enabled(self):
        """
        bool: Indicates whether encryption is enabled.
        """
        return self.config.get("encryption_enabled", False)

    @encryption_enabled.setter
    def encryption_enabled(self, value):
        """
        Set the encryption enabled status and save it to the configuration file.

        Args:
            value (bool): New encryption enabled status.
        """
        self.config["encryption_enabled"] = value
        self.save_config()

    @property
    def get_max_username_length(self):
        """
        int: Maximum allowed length for usernames.
        """
        return self.MAX_USERNAME_LENGTH

    @property
    def get_max_message_length(self):
        """
        int: Maximum allowed length for chat messages.
        """
        return self.MAX_MESSAGE_LENGTH
