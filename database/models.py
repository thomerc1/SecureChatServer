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
Secure Chat Server Database Models

This module defines the SQLAlchemy models for the Secure Chat Server application.
It includes the UsersModel and ChatModel classes for storing user and chat information.

Author: Group A

Dependencies:
- Flask-SQLAlchemy
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UsersModel(db.Model):
    """
    Model for storing user information.

    Fields:
    - id: Primary key for the user record.
    - username: User's username. MAX 50 chars
    - authenticated: Boolean indicating whether the user successfully entered the encryption password.
    - ssh_key_setup: Boolean indicating whether the user has set up an SSH key.
    """

    __tablename__ = "users"
    __bind_key__ = "users_db"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    ssh_key_setup = db.Column(db.Boolean, default=False)

    def __init__(self, username, authenticated=False, ssh_key_setup=False):
        self.username = username
        self.authenticated = authenticated
        self.ssh_key_setup = ssh_key_setup

    @staticmethod
    def add_user(username, authenticated=False, ssh_key_setup=False):
        """
        Add a new user to the database.

        Args:
            username (str): The username of the new user.
            authenticated (bool, optional): Whether the user is authenticated (default is False).
            ssh_key_setup (bool, optional): Whether the user has set up an SSH key (default is False).
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
    def is_authenticated(username):
        """
        Check if a user with the given username has been authenticated.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        user = UsersModel.query.filter_by(username=username).first()
        return user is not None and user.authenticated

    @staticmethod
    def has_uploaded_ssh_key(username):
        """
        Check if a user with the given username has uploaded an SSH key.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the user has uploaded an SSH key, False otherwise.
        """
        user = UsersModel.query.filter_by(username=username).first()
        return user is not None and user.ssh_key_setup


class ChatModel(db.Model):
    """
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
