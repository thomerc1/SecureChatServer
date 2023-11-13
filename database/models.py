"""
Course Name: CMSC495 7384
Project: CMSC495 Secure Chat Server
Group: A
Date: Nov 23'
Platform: Debian Linux
Dependency: Python 3.10 +
=======================================================
Description:
Secure Chat Server Database Models

This module defines the SQLAlchemy models for the Secure Chat Server application.
It includes the UsersModel and ChatModel classes for storing user and chat information.

Dependencies:
- Flask-SQLAlchemy
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UsersModel(db.Model):
    """
    SQLAlchemy Model for storing user information.
    """

    __tablename__ = "users"
    __bind_key__ = "users_db"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    ssh_key_setup = db.Column(db.Boolean, default=False)

    def __init__(self, username: str, authenticated: bool = False, ssh_key_setup: bool = False) -> None:
        """
        Author:
            Eric Thomas

        Description:
            Constructor for UsersModel.

        Args:
            username (str): The username of the user.
            authenticated (bool, optional): User's authentication status. Defaults to False.
            ssh_key_setup (bool, optional): User's SSH key setup status. Defaults to False.
        """
        self.username = username
        self.authenticated = authenticated
        self.ssh_key_setup = ssh_key_setup

    @staticmethod
    def add_user(username: str, authenticated: bool = False, ssh_key_setup: bool = False) -> NoReturn:
        """
        Author:
            Eric Thomas

        Description:
            Static method to add a new user to the database.

        Args:
            username (str): Username of the new user.
            authenticated (bool, optional): Authentication status. Defaults to False.
            ssh_key_setup (bool, optional): SSH key setup status. Defaults to False.

        Raises:
            Exception: If any database operation fails.
        """
        try:
            new_user = UsersModel(username=username, authenticated=authenticated, ssh_key_setup=ssh_key_setup)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # TODO: Handle the exception here (e.g., log the error)
            raise e

    @staticmethod
    def is_authenticated(username: str) -> bool:
        """
        Author:
            Eric Thomas

        Description:
            Static method to check if a user is authenticated.

        Args:
            username (str): Username to check for authentication.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        user = UsersModel.query.filter_by(username=username).first()
        return user is not None and user.authenticated

    @staticmethod
    def has_uploaded_ssh_key(username: str) -> bool:
        """
        Author:
            Eric Thomas

        Description:
            Static method to check if a user has uploaded an SSH key.

        Args:
            username (str): Username to check for SSH key upload.

        Returns:
            bool: True if the user has uploaded an SSH key, False otherwise.
        """
        user = UsersModel.query.filter_by(username=username).first()
        return user is not None and user.ssh_key_setup


class ChatModel(db.Model):
    """
    Author: Eric Thomas

    Model for storing chat information.

    Fields:
    - id: Primary key for the chat record.
    - message: The chat message.
    """

    __tablename__ = "chat"
    __bind_key__ = "chat_db"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)

    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    # Example usage for ServerConfig class
    from config.server_config import ServerConfig

    server_config = ServerConfig(ssh_enabled=True, encryption_enabled=True)
    server_config.print_params()
    print(f"Max Username Length: {server_config.get_max_username_length()}")
    print(f"Max Message Length: {server_config.get_max_message_length()}")

    # Example usage for UsersModel class
    user1 = UsersModel(username="user1")
    user2 = UsersModel(username="user2", authenticated=True)
    user3 = UsersModel(username="user3", ssh_key_setup=True)

    # Adding users to the database
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

    # Check if a user exists
    username_to_check = "user1"
    if UsersModel.user_exists(username_to_check):
        print(f"{username_to_check} exists in the database.")

    # Check if a user is authenticated
    if UsersModel.is_authenticated(username_to_check):
        print(f"{username_to_check} is authenticated.")

    # Check if a user has uploaded an SSH key
    if UsersModel.has_uploaded_ssh_key(username_to_check):
        print(f"{username_to_check} has uploaded an SSH key.")
